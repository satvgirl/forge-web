// Forge marketing site: serves public/ as static assets (handled automatically
// by the [assets] binding before this script ever runs — see wrangler.toml) and
// implements the waitlist API. Only requests with no matching static file reach
// fetch() below: /api/* routes, and genuine 404s.

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/waitlist" && request.method === "POST") {
      return handleWaitlistSubmit(request, env);
    }

    if (url.pathname === "/api/waitlist/export" && request.method === "GET") {
      return handleExport(request, env);
    }

    return serveNotFound(request, env);
  },
};

async function parseBody(request) {
  const contentType = request.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    try {
      return await request.json();
    } catch {
      return {};
    }
  }
  if (
    contentType.includes("application/x-www-form-urlencoded") ||
    contentType.includes("multipart/form-data")
  ) {
    const form = await request.formData();
    return { email: form.get("email"), company: form.get("company") };
  }
  return {};
}

function wantsJson(request) {
  return (request.headers.get("accept") || "").includes("application/json");
}

async function handleWaitlistSubmit(request, env) {
  const body = await parseBody(request);
  const email = String(body.email || "").trim().toLowerCase();
  const honeypot = String(body.company || "").trim();

  // Bots that fill the hidden "company" field get a fake success — no store,
  // no signal back to them that they were caught.
  if (honeypot) {
    return respond(request, true, null);
  }

  if (!email || !EMAIL_RE.test(email) || email.length > 320) {
    return respond(request, false, "Enter a valid email address.");
  }

  await env.WAITLIST.put(
    email,
    JSON.stringify({ email, joinedAt: new Date().toISOString() })
  );

  return respond(request, true, null);
}

function respond(request, ok, error) {
  if (wantsJson(request)) {
    return new Response(JSON.stringify({ ok, error }), {
      status: ok ? 200 : 400,
      headers: { "content-type": "application/json;charset=utf-8" },
    });
  }
  return htmlFallback(ok, error);
}

function htmlFallback(ok, error) {
  const heading = ok ? "You're on the list" : "Something went wrong";
  const message = ok
    ? "We'll email you when the beta opens."
    : error || "Please go back and try again.";
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${heading} — Forge</title>
<style>
  :root { --bg:#f9f7f3; --text:#2b2b2b; --muted:#6b6b6b; --accent:#b06a3b; --link:#9a5a2f; }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#1a1917; --text:#e9e6e0; --muted:#a5a09a; --accent:#d9945f; --link:#e0a276; }
  }
  body { margin:0; min-height:100vh; display:grid; place-items:center; background:var(--bg); color:var(--text);
    font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
  main { text-align:center; padding:40px 24px; }
  .eyebrow { text-transform:uppercase; letter-spacing:0.14em; font-size:12px; font-weight:600; color:var(--accent); margin:0 0 12px; }
  h1 { font-size:28px; margin:0 0 10px; }
  p { color:var(--muted); margin:0 0 20px; }
  a { color:var(--link); }
</style>
</head>
<body>
<main>
  <p class="eyebrow">Forge</p>
  <h1>${heading}</h1>
  <p>${message}</p>
  <a href="/">Back to forge-app.ca</a>
</main>
</body>
</html>`;
  return new Response(html, {
    status: ok ? 200 : 400,
    headers: { "content-type": "text/html;charset=utf-8" },
  });
}

async function handleExport(request, env) {
  const auth = request.headers.get("authorization") || "";
  const token = auth.startsWith("Bearer ") ? auth.slice(7) : "";
  if (!env.ADMIN_TOKEN || token !== env.ADMIN_TOKEN) {
    return new Response("Unauthorized", { status: 401 });
  }

  const rows = [["email", "joined_at"]];
  let cursor;
  do {
    const page = await env.WAITLIST.list({ cursor });
    for (const key of page.keys) {
      const raw = await env.WAITLIST.get(key.name);
      const entry = raw ? JSON.parse(raw) : { email: key.name, joinedAt: "" };
      rows.push([entry.email, entry.joinedAt]);
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);

  const csv = rows.map((r) => r.map(csvEscape).join(",")).join("\n");
  return new Response(csv, {
    headers: {
      "content-type": "text/csv;charset=utf-8",
      "content-disposition": 'attachment; filename="forge-waitlist.csv"',
    },
  });
}

function csvEscape(value) {
  const s = String(value ?? "");
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

async function serveNotFound(request, env) {
  const notFound = await env.ASSETS.fetch(new URL("/404.html", request.url));
  return new Response(notFound.body, {
    status: 404,
    headers: notFound.headers,
  });
}

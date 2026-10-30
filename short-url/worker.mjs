import script from "../install.sh";

export default {
  fetch(request) {
    const url = new URL(request.url);
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed\n", {status: 405, headers: {Allow: "GET, HEAD"}});
    }
    if (url.pathname === "/" || url.pathname === "/install.sh") {
      return new Response(request.method === "HEAD" ? null : script, {headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Cache-Control": "public, max-age=300",
        "X-Content-Type-Options": "nosniff",
        "X-Kit-Version": "0.2.0"
      }});
    }
    if (url.pathname === "/source") {
      return Response.redirect("https://github.com/Shinick-Han/agent-exam-kit", 302);
    }
    return new Response("Not found\n", {status: 404});
  }
};

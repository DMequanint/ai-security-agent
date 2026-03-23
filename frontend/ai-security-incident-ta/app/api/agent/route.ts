export async function POST(req: Request) {
  const body = await req.json()

  const res = await fetch("http://backend:8000/agent/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })

  return new Response(res.body, {
    headers: { "Content-Type": "text/plain" },
  })
}

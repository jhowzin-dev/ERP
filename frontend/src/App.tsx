function App() {
  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col items-center justify-center gap-4 p-8">
      <h1 className="text-4xl font-semibold tracking-tight">SG-MULTIDIA</h1>
      <p className="text-zinc-400">
        Frontend React + TypeScript + Vite + Tailwind — scaffold inicial.
      </p>
      <a
        href="/api/actuator/health"
        className="text-sm text-zinc-500 underline underline-offset-4 hover:text-zinc-300"
      >
        API health: /api/actuator/health
      </a>
    </main>
  )
}

export default App
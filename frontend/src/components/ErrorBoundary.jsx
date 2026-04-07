import React from 'react'

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, info) {
    // You could log to a remote service here
    console.error('Uncaught error:', error, info)
  }

  render() {
    if (!this.state.hasError) return this.props.children

    return (
      <div className="min-h-screen flex items-center justify-center p-6">
        <div className="max-w-xl text-center bg-coal-800 p-8 rounded-xl border border-white/5">
          <h2 className="text-2xl text-white font-bold mb-2">Something went wrong</h2>
          <p className="text-gray-400 mb-4">An unexpected error occurred while rendering the app.</p>
          <pre className="text-xs text-red-400 text-left break-words p-2 bg-black/30 rounded mb-4">{String(this.state.error)}</pre>
          <div className="flex justify-center gap-3">
            <button className="btn-primary px-4 py-2" onClick={() => window.location.reload()}>Reload</button>
          </div>
        </div>
      </div>
    )
  }
}

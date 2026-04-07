export function getErrorMessage(err) {
  if (!err) return null

  // Axios response body
  const resp = err.response?.data
  if (resp) {
    // If detail is array of validation errors
    if (Array.isArray(resp.detail) && resp.detail.length > 0) {
      // Try to extract first message
      const first = resp.detail[0]
      if (typeof first === 'string') return first
      if (first?.msg) return first.msg
    }
    // If detail is a string
    if (typeof resp.detail === 'string') return resp.detail
    // If error has message field
    if (resp.message) return resp.message
  }

  // Plain axios error message
  if (err.message) return err.message

  // Fallback stringify (safe)
  try {
    return JSON.stringify(err)
  } catch {
    return String(err)
  }
}

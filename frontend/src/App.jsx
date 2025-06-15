import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('Loading...')
  const [users, setUsers] = useState([])
  const [health, setHealth] = useState(null)

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  const environment = import.meta.env.VITE_ENVIRONMENT || 'development'

  useEffect(() => {
    // Test API connection
    fetch(`${apiUrl}/api/hello`)
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(err => setMessage('Failed to connect to API'))

    // Check health status
    fetch(`${apiUrl}/health`)
      .then(res => res.json())
      .then(data => setHealth(data.status))
      .catch(err => setHealth('unhealthy'))

    // Get users
    fetch(`${apiUrl}/api/users`)
      .then(res => res.json())
      .then(data => setUsers(data))
      .catch(err => console.error('Failed to fetch users:', err))
  }, [apiUrl])

  return (
    <div className="app">
      <header className="app-header">
        <h1>Starter Web App</h1>
        <p className="subtitle">Full-stack template with FastAPI + React</p>
        <div className="env-info">
          <span className={`env-badge ${environment}`}>
            {environment.toUpperCase()}
          </span>
          <span className="api-url">API: {apiUrl}</span>
        </div>
      </header>

      <main className="app-main">
        <section className="status-section">
          <h2>Backend Status</h2>
          <div className="status-grid">
            <div className="status-card">
              <h3>API Message</h3>
              <p>{message}</p>
            </div>
            <div className="status-card">
              <h3>Health Check</h3>
              <p className={`health-status ${health}`}>
                {health || 'checking...'}
              </p>
            </div>
          </div>
        </section>

        <section className="users-section">
          <h2>Users ({users.length})</h2>
          {users.length > 0 ? (
            <div className="users-grid">
              {users.map(user => (
                <div key={user.id} className="user-card">
                  <h3>{user.name}</h3>
                  <p>{user.email}</p>
                  <span className={`status ${user.is_active ? 'active' : 'inactive'}`}>
                    {user.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-users">No users found. Add some users to the database!</p>
          )}
        </section>
      </main>
    </div>
  )
}

export default App

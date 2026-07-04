import React from 'react';

const Login: React.FC = () => {
  return (
    <div className="login-page">
      <form style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Email</label>
          <input type="email" className="input-field" placeholder="Enter your email" />
        </div>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Password</label>
          <input type="password" className="input-field" placeholder="Enter your password" />
        </div>
        <button type="button" className="btn-primary" style={{ marginTop: '1rem' }}>Sign In</button>
      </form>
      <p style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.9rem' }}>
        Don't have an account? <a href="/register" style={{ color: 'var(--accent-primary)', textDecoration: 'none' }}>Register</a>
      </p>
    </div>
  );
};

export default Login;

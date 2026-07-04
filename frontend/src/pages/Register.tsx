import React from 'react';

const Register: React.FC = () => {
  return (
    <div className="register-page">
      <form style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Username</label>
          <input type="text" className="input-field" placeholder="Choose a username" />
        </div>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Email</label>
          <input type="email" className="input-field" placeholder="Enter your email" />
        </div>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Password</label>
          <input type="password" className="input-field" placeholder="Create a password" />
        </div>
        <button type="button" className="btn-primary" style={{ marginTop: '1rem' }}>Create Account</button>
      </form>
      <p style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.9rem' }}>
        Already have an account? <a href="/login" style={{ color: 'var(--accent-primary)', textDecoration: 'none' }}>Sign In</a>
      </p>
    </div>
  );
};

export default Register;

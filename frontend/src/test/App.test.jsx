// frontend/src/test/App.test.jsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../App';

describe('App', () => {
  it('renders the main heading', () => {
    render(<App />);
    // Check if the "Task Manager" heading is on the page
    expect(screen.getByRole('heading', { name: /Task Manager/i })).toBeInTheDocument();
  });
});
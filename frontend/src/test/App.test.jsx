// frontend/src/test/App.test.jsx

import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import App from '../App';

beforeEach(() => {
  global.fetch = vi.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve([{ id: 1, title: 'Mocked Task' }]),
    })
  );
});

describe('App', () => {
  // FIX: The test is now an 'async' function.
  it('renders the main heading and fetched tasks', async () => {
    render(<App />);

    // FIX: We use 'findByRole' which waits for the element to appear after the
    // state update from fetch has completed. This resolves the act() warning.
    const heading = await screen.findByRole('heading', { name: /Task Manager/i });
    expect(heading).toBeInTheDocument();

    // We can also verify that our mocked task is rendered.
    const taskItem = await screen.findByText('Mocked Task');
    expect(taskItem).toBeInTheDocument();
  });
});
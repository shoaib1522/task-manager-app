// frontend/src/test/setup.js

// FIX: Removed 'expect' from this line as it was unused.
import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import '@testing-library/jest-dom';

afterEach(() => {
  cleanup();
});
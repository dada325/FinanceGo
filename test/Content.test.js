// frontend/src/tests/Content.test.js

import { render, screen } from '@testing-library/react';
import Content from '../Content';

test('renders content', () => {
  render(<Content />);
  const linkElement = screen.getByText(/Welcome to our News Feed App/i);
  expect(linkElement).toBeInTheDocument();
});

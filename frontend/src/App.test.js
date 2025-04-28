import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';
import axios from 'axios';

jest.mock('axios');

describe('App Component', () => {
  test('renders the app title', () => {
    render(<App />);
    const titleElement = screen.getByText(/Questionnaire Scanner/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('handles file upload', () => {
    render(<App />);
    const fileInput = screen.getByLabelText(/upload/i);
    const file = new File(['dummy content'], 'example.png', { type: 'image/png' });

    fireEvent.change(fileInput, { target: { files: [file] } });
    expect(fileInput.files[0]).toBe(file);
    expect(fileInput.files).toHaveLength(1);
  });

  test('processes image on button click', async () => {
    axios.post.mockResolvedValue({ data: { extractedData: 'Test Data' } });

    render(<App />);
    const processButton = screen.getByText(/Process Image/i);

    fireEvent.click(processButton);
    const result = await screen.findByText(/Test Data/i);
    expect(result).toBeInTheDocument();
  });
});

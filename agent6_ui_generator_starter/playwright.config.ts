import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: 'tests/E2E',
  use: { baseURL: process.env.E2E_BASE_URL || 'http://localhost:8000' },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});

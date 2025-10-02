import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  vus: Number(__ENV.VUS || 10),
  duration: __ENV.DURATION || '1m',
  thresholds: {
    http_req_failed: ['rate<=0.01']
  }
};

const BASE = __ENV.BASE_URL || 'http://localhost:8000';

export default function () {
  const endpoints = JSON.parse(__ENV.ENDPOINTS || '[]');
  for (const ep of endpoints) {
    const res = http.request(ep.method || 'GET', BASE + ep.path);
    check(res, { 'status is 2xx': (r) => r.status >= 200 && r.status < 300 });
    sleep(0.2);
  }
}

import type { APIRoute } from 'astro';
import { buildRss } from '../../lib/rss-feed';

export const GET: APIRoute = ({ site }) => buildRss('pt', site);

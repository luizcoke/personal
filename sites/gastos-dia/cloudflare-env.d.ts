declare namespace Cloudflare {
  interface Env {
    DB?: D1Database;
    BUCKET?: R2Bucket;
    SITE_SERVICE_TOKEN?: string;
  }
}

import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const publicRoot = join(process.cwd(), "public");
const pressPage = join(publicRoot, "press", "index.html");
const html = readFileSync(pressPage, "utf8");
const urls = new Set();
const attributePattern = /(?:href|src)=["']?(\/[^"' >]+)/g;

for (const match of html.matchAll(attributePattern)) {
  urls.add(match[1]);
}

const missing = [];

for (const url of [...urls].sort()) {
  const pathname = new URL(url, "https://example.test").pathname;
  const relativePath = pathname.replace(/^\/+/, "");
  const target = url.endsWith("/")
    ? join(publicRoot, relativePath, "index.html")
    : join(publicRoot, relativePath);

  if (!existsSync(target)) {
    missing.push(url);
  }
}

console.log(`Checked ${urls.size} local press-page links and assets.`);

if (missing.length > 0) {
  console.error(`Missing:\n${missing.join("\n")}`);
  process.exit(1);
}

console.log("All local press-page links and assets resolve.");

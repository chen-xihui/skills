#!/usr/bin/env node
/**
 * Lightweight shell guard for middleware skills (ECC-style hook).
 * Blocks obvious shell injection in paas-cli / bianque invocations.
 */
const input = JSON.parse(require("fs").readFileSync(0, "utf8"));
const cmd = String(input.command || input.shellCommand || "");

// Do not match `&&` (common shell chaining); focus on injection primitives.
const injection = /(;|\$\(|`|\$\{|\|\s*(?!\|))/;
const relevant = /\b(paas-cli|bianque\.py|skills\/paas-cli|skills\/bianque)\b/.test(cmd);

if (relevant && injection.test(cmd)) {
  console.error(
    JSON.stringify({
      permission: "deny",
      userMessage:
        "命令包含 shell 元字符，已被 cli-security-rules 拦截。请仅使用白名单参数。",
    })
  );
  process.exit(2);
}

console.log(JSON.stringify({ permission: "allow" }));
process.exit(0);

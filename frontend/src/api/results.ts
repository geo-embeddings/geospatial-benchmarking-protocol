import type { components } from "./types";

type Result = components["schemas"]["Result"];

export async function listResults(tag?: string): Promise<Result[]> {
  const url = tag
    ? `/api/results/?tag=${encodeURIComponent(tag)}`
    : "/api/results/";
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch results");
  return res.json();
}

export async function getResult(id: string): Promise<Result> {
  const res = await fetch(`/api/results/${id}`);
  if (!res.ok) throw new Error("Failed to fetch result");
  return res.json();
}

export async function createResult(
  result: Omit<Result, "id">,
): Promise<{ id: string }> {
  const res = await fetch("/api/results/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(result),
  });
  if (!res.ok) throw new Error("Failed to create result");
  return res.json();
}

export async function deleteResult(id: string): Promise<void> {
  const res = await fetch(`/api/results/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete result");
}

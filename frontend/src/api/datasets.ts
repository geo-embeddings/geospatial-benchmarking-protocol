import type { components } from "./types";

type Dataset = components["schemas"]["Dataset"];

export async function listDatasets(): Promise<Dataset[]> {
  const res = await fetch("/api/datasets/");
  if (!res.ok) throw new Error("Failed to fetch datasets");
  return res.json();
}

export async function getDataset(id: string): Promise<Dataset> {
  const res = await fetch(`/api/datasets/${id}`);
  if (!res.ok) throw new Error("Failed to fetch dataset");
  return res.json();
}

export async function createDataset(
  dataset: Omit<Dataset, "id">,
): Promise<{ id: string }> {
  const res = await fetch("/api/datasets/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dataset),
  });
  if (!res.ok) throw new Error("Failed to create dataset");
  return res.json();
}

export async function deleteDataset(id: string): Promise<void> {
  const res = await fetch(`/api/datasets/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete dataset");
}

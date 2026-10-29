"""Export the Git-native Postman YAML artifacts as Desktop-importable v2.1 JSON."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

import yaml


ROOT = Path(__file__).resolve().parents[1]
COLLECTION_ROOT = ROOT / "postman" / "collections" / "BookIt API"
ENVIRONMENT_SOURCE = ROOT / "postman" / "environments" / "BookIt Local.environment.yaml"
EXPORT_ROOT = ROOT / "postman" / "imports"


def title_from_filename(path: Path) -> str:
    return path.name.removesuffix(".request.yaml").replace("_", " ").title()


def request_from_yaml(path: Path) -> dict:
    source = yaml.safe_load(path.read_text(encoding="utf-8"))
    headers = [{"key": key, "value": value} for key, value in source.get("headers", {}).items()]
    request = {"method": source["method"], "header": headers, "url": {"raw": source["url"]}}

    body = source.get("body")
    if body:
        if body["type"] == "json":
            request["body"] = {"mode": "raw", "raw": body["content"], "options": {"raw": {"language": "json"}}}
        elif body["type"] == "urlencoded":
            content = body["content"]
            fields = content if isinstance(content, list) else [
                {"key": key, "value": value} for key, value in content.items()
            ]
            request["body"] = {
                "mode": "urlencoded",
                "urlencoded": [
                    {"key": field["key"], "value": str(field.get("value", "")), "disabled": field.get("disabled", False)}
                    for field in fields
                ],
            }

    if source.get("auth", {}).get("type") == "bearer":
        request["auth"] = {"type": "bearer", "bearer": [{"key": "token", "value": source["auth"]["credentials"]["token"], "type": "string"}]}

    item = {"name": source.get("name", title_from_filename(path)), "request": request}
    after_response = next((script for script in source.get("scripts", []) if script["type"] == "afterResponse"), None)
    if after_response:
        item["event"] = [{"listen": "test", "script": {"type": "text/javascript", "exec": after_response["code"].splitlines()}}]
    return item


def ordered_requests(folder: Path) -> list[dict]:
    files = []
    for request_file in folder.glob("*.request.yaml"):
        data = yaml.safe_load(request_file.read_text(encoding="utf-8"))
        files.append((data.get("order", 0), request_file.name, request_from_yaml(request_file)))
    return [item for _, _, item in sorted(files)]


def export() -> None:
    definition = yaml.safe_load((COLLECTION_ROOT / ".resources" / "definition.yaml").read_text(encoding="utf-8"))
    folders = []
    for child in COLLECTION_ROOT.iterdir():
        if child.is_dir() and not child.name.startswith(".") and child.name != "postman":
            requests = ordered_requests(child)
            if requests:
                folders.append({"name": child.name.title(), "item": requests})

    collection = {
        "info": {"_postman_id": str(uuid5(NAMESPACE_URL, "bookit-api")), "name": "BookIt API", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
        "variable": [{"key": key, "value": value, "type": "string"} for key, value in definition.get("variables", {}).items()],
        "item": folders,
    }
    environment_source = yaml.safe_load(ENVIRONMENT_SOURCE.read_text(encoding="utf-8"))
    environment = {
        "id": str(uuid5(NAMESPACE_URL, "bookit-local-environment")),
        "name": environment_source["name"],
        "values": [
            {"key": value["key"], "value": value.get("value", ""), "type": "default", "enabled": value.get("enabled", True)}
            for value in environment_source["values"]
        ],
        "_postman_variable_scope": "environment",
        "_postman_exported_using": "BookIt export script",
    }
    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)
    (EXPORT_ROOT / "BookIt API.postman_collection.json").write_text(json.dumps(collection, indent=2) + "\n", encoding="utf-8")
    (EXPORT_ROOT / "BookIt Local.postman_environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    export()

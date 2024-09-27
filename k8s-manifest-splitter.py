import yaml
import os
import argparse

def split_k8s_manifests(manifest_file):
    # Create a directory to store the split files
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    with open(manifest_file, 'r') as file:
        # Load the entire YAML file
        documents = yaml.safe_load_all(file)

        for index, doc in enumerate(documents):
            if doc is None:
                continue
            kind = doc.get("kind", f"unknown_{index}")  # Use 'unknown_{index}' if 'kind' is not present
            filename = f"{kind.lower()}_{index}.yaml"  # Lowercase the kind and append index for uniqueness
            filepath = os.path.join(output_dir, filename)
            # Write each document to its respective file
            with open(filepath, 'w') as output_file:
                yaml.dump(doc, output_file)
            print(f"Created: {filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split Kubernetes manifest file into separate files.")
    parser.add_argument('manifest_file', type=str, help="Path to the joined Kubernetes manifest file.")

    args = parser.parse_args()
    split_k8s_manifests(args.manifest_file)

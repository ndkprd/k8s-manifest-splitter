import yaml
import os
import argparse

# Define the order in which the resources should appear
RESOURCE_ORDER = {
    'ServiceAccount': 1,
    'Role': 2,
    'ClusterRole': 3,
    'RoleBinding': 4,
    'ClusterRoleBinding': 5,
    'Deployment': 100,
    'DaemonSet': 100,
    'StatefulSet': 100,
    'Pod': 100,
}

def get_resource_order(kind):
    """ Return the order based on resource kind. Defaults to high number for unordered resources. """
    return RESOURCE_ORDER.get(kind, 99)

def generate_kustomize(manifest_file):

    base_dir = "base"
    os.makedirs(base_dir, exist_ok=True)

    # Get the target filename (without extension) to create a subfolder inside base
    target_filename = os.path.splitext(os.path.basename(manifest_file))[0]
    output_dir = os.path.join(base_dir, target_filename)
    os.makedirs(output_dir, exist_ok=True)

    resources = []  # List to store the filenames for kustomization.yaml
    docs_with_order = []  # To store documents with their order for sorting

    with open(manifest_file, 'r') as file:
        # Load the entire YAML file
        documents = yaml.safe_load_all(file)

        for index, doc in enumerate(documents):
            if doc is None:
                continue

            # Extract 'kind' and 'metadata.name', fallback to index if name not present
            kind = doc.get("kind", f"unknown_{index}")
            name = doc.get("metadata", {}).get("name", f"unnamed_{index}")

            # Determine the resource's order based on its kind
            order = get_resource_order(kind)
            docs_with_order.append((order, kind, name, doc))  # Store tuple with order and doc info

    # Sort documents based on the order
    docs_with_order.sort(key=lambda x: x[0])

    # After sorting, generate the YAML files
    for index, (order, kind, name, doc) in enumerate(docs_with_order):
        # Create filename in the format 'kind_name.yaml'
        filename = f"{kind.lower()}_{name}.yaml"
        filepath = os.path.join(output_dir, filename)

        # Write each document to its respective file
        with open(filepath, 'w') as output_file:
            output_file.write("---\n\n")  # Write the '---' separator
            yaml.dump(doc, output_file)
        print(f"Created: {filepath}")

        # Add the file path to the resources list
        resources.append(f"  - {target_filename}/{filename}")  # Add 2-space indent before "-"

    # Create the kustomization.yaml inside base_dir
    kustomization_file = os.path.join(base_dir, "kustomization.yaml")
    with open(kustomization_file, 'w') as kustomization:
        # Add "---\n\n" before resources
        kustomization.write("---\n\n")
        kustomization.write("resources:\n")
        
        # Write each resource with the proper indent
        for resource in resources:
            kustomization.write(f"{resource}\n")

    print(f"Created: {kustomization_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Kustomize manifests from a single Kubernetes manifest file.")
    parser.add_argument('manifest_file', type=str, help="Path to the joined Kubernetes manifest file.")

    args = parser.parse_args()
    generate_kustomize(args.manifest_file)

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
    overlays_dir = "overlays"
    
    # Create base and overlays directories
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(overlays_dir, exist_ok=True)

    # Create overlays subdirectories
    for env in ['development', 'staging', 'production']:
        env_dir = os.path.join(overlays_dir, env)
        os.makedirs(env_dir, exist_ok=True)

        # Create kustomization.yaml for each overlay environment using 'resources' instead of 'bases'
        overlay_kustomization_file = os.path.join(env_dir, 'kustomization.yaml')
        with open(overlay_kustomization_file, 'w') as overlay_kustomization:
            overlay_kustomization.write("---\n\n")
            overlay_kustomization.write(f"resources:\n  - ../../base\n")
        print(f"Created: {overlay_kustomization_file}")

    # Get the target filename (without extension) to create a subfolder inside base
    target_filename = os.path.splitext(os.path.basename(manifest_file))[0]
    output_dir = os.path.join(base_dir, target_filename)
    os.makedirs(output_dir, exist_ok=True)

    resource_folders = []  # To store the folder paths for base kustomization.yaml
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

    # After sorting, generate the YAML files inside their resource type folder
    resource_type_paths = {}
    
    for index, (order, kind, name, doc) in enumerate(docs_with_order):
        # Create folder structure: ./base/{target_filename}/{kind}
        kind_dir = os.path.join(output_dir, kind.lower())
        os.makedirs(kind_dir, exist_ok=True)

        # Create filename in the format '{kind}_{name}.yaml'
        filename = f"{kind.lower()}_{name}.yaml"
        filepath = os.path.join(kind_dir, filename)

        # Write each document to its respective file
        with open(filepath, 'w') as output_file:
            output_file.write("---\n\n")  # Write the '---' separator
            yaml.dump(doc, output_file)
        print(f"Created: {filepath}")

        # Track the resource type folder for base kustomization.yaml
        if kind_dir not in resource_type_paths:
            resource_type_paths[kind_dir] = []
        
        # Add the file path to the resource type folder
        resource_type_paths[kind_dir].append(f"  - {filename}")

    # Create kustomization.yaml in each resource type folder
    for kind_dir, resources in resource_type_paths.items():
        resource_kustomization_file = os.path.join(kind_dir, 'kustomization.yaml')
        with open(resource_kustomization_file, 'w') as resource_kustomization:
            resource_kustomization.write("---\n\n")
            resource_kustomization.write(f"resources:\n")
            for resource in resources:
                resource_kustomization.write(f"{resource}\n")
        print(f"Created: {resource_kustomization_file}")

    # Create the main kustomization.yaml inside base_dir
    base_kustomization_file = os.path.join(base_dir, "kustomization.yaml")
    with open(base_kustomization_file, 'w') as base_kustomization:
        base_kustomization.write("---\n\n")
        base_kustomization.write("resources:\n")
        
        # Write each resource type folder with the proper indent
        for kind_dir in resource_type_paths.keys():
            relative_kind_dir = os.path.relpath(kind_dir, base_dir)
            base_kustomization.write(f"  - {relative_kind_dir}\n")

    print(f"Created: {base_kustomization_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Kustomize manifests from a single Kubernetes manifest file.")
    parser.add_argument('manifest_file', type=str, help="Path to the joined Kubernetes manifest file.")

    args = parser.parse_args()
    generate_kustomize(args.manifest_file)

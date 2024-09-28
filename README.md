# kustomize-generator

Simple script that generate Kustomize base manifests from a single Kubernetes manifest file.

## Usage

1. Copy/download the script;
2. Run it against your joined manifest file:

```bash
python kustomize_generator.py <your-file>
```

3. Check the output in `./base`.

You can see the example in [example](example/) folder, where I generate a base Kustomize [ingress-nginx-controller](https://kubernetes.github.io/ingress-nginx/) based on their static joined manifests.

>[!Note]
> The script will use the target file name as the base folder name that contains all the splitted resources, e.g. `ingress-nginx.yaml` will create `base/ingress-nginx/*.yaml`.

## Use Case Example

1. Converting single Kubernetes manifests to Kustomize base manifests.

```bash
wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.2/deploy/static/provider/cloud/deploy.yaml

python k8s-manifest-splitter.py deploy.yaml
```


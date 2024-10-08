# kustomize-generator

Simple script that generate Kustomize base manifests from a single Kubernetes manifest file.

## Usage

1. Copy/download the script;
2. Run it against your joined manifest file:

```bash
python kustomize_generator.py <your-file>
```

Or if you want to use it directly:

```bash
curl -s https://raw.githubusercontent.com/ndkprd/kustomize-generator/refs/heads/main/kustomize_generator.py | python - <your-file>
```

3. Check the output in `./base`.

You can see the example in [example](example/) folder, where I generate a base Kustomize [ingress-nginx-controller](https://kubernetes.github.io/ingress-nginx/) based on their static joined manifests.

>[!Note]
> The script will use the target file name as the base folder name that contains all the splitted resources, e.g. `ingress-nginx.yaml` will create `base/ingress-nginx/*.yaml`.

## Use Case Example

1. Converting single Kubernetes manifests to Kustomize base manifests (case example: ingress-nginx).

```bash
# pull remote manifests to local
curl https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.2/deploy/static/provider/cloud/deploy.yaml > ingress-nginx.yaml

# convert it into kustomize-friendly format
python kustomize-generator.py ingress-nginx.yaml
```

2. Converting Helm Charts to Kustomize base manifests (case example: [authentik](https://goauthentik.io)).

```bash
# template out the helm charts
helm template authentik authentik/authentik > authentik.yaml

# convert it into kustomize-friendly format
python kustomize-generator.py authentik.yaml
```

3. Converting export result from [ketall](https://github.com/corneliusweig/ketall) plugin (case example: ingress-nginx).

```bash
# export resources
kubectl get-all -n ingress-nginx > ingress-nginx.yaml

# convert it into kustomize-friendly format
python kustomize-generator.py ingress-nginx.yaml
```

## LICENSE

MIT

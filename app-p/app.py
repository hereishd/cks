from flask import Flask, render_template, request, jsonify
from kubernetes import client, config
from kubernetes.client.rest import ApiException

app = Flask(__name__)

@app.route('/')
def index():
    """Render the dashboard with a textbox and button."""
    return render_template('index.html')

@app.route('/list_pods', methods=['POST'])
def list_pods():
    """List all pods in the Kubernetes cluster."""
    token = request.json.get('token')

    if not token:
        return jsonify({"error": "Service account token is required."}), 400

    try:
        # Configure API client with the provided token
        configuration = client.Configuration()
        configuration.host = "https://kubernetes.default.svc"
        configuration.verify_ssl = False  # Disable SSL verification (adjust as needed)
        configuration.api_key = {"authorization": f"Bearer {token}"}

        # Create an API client
        api_client = client.ApiClient(configuration)
        v1 = client.CoreV1Api(api_client)

        # Fetch the pods
        pods = v1.list_pod_for_all_namespaces()
        pod_list = [{"name": pod.metadata.name, "namespace": pod.metadata.namespace} for pod in pods.items]

        return jsonify(pod_list)

    except ApiException as e:
        return jsonify({"error": f"API exception: {e.reason}"}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/list_services', methods=['POST'])
def list_services():
    """List all services in the Kubernetes cluster."""
    token = request.json.get('token')

    if not token:
        return jsonify({"error": "Service account token is required."}), 400

    try:
        # Configure API client with the provided token
        configuration = client.Configuration()
        configuration.host = "https://kubernetes.default.svc"
        configuration.verify_ssl = False  # Disable SSL verification (adjust as needed)
        configuration.api_key = {"authorization": f"Bearer {token}"}

        # Create an API client
        api_client = client.ApiClient(configuration)
        v1 = client.CoreV1Api(api_client)

        # Fetch the services
        services = v1.list_service_for_all_namespaces()
        service_list = [{"name": service.metadata.name, "namespace": service.metadata.namespace} for service in services.items]

        return jsonify(service_list)

    except ApiException as e:
        return jsonify({"error": f"API exception: {e.reason}"}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/list_deployments', methods=['POST'])
def list_deployments():
    """List all deployments in the Kubernetes cluster."""
    token = request.json.get('token')

    if not token:
        return jsonify({"error": "Service account token is required."}), 400

    try:
        # Configure API client with the provided token
        configuration = client.Configuration()
        configuration.host = "https://kubernetes.default.svc"
        configuration.verify_ssl = False  # Disable SSL verification (adjust as needed)
        configuration.api_key = {"authorization": f"Bearer {token}"}

        # Create an API client
        api_client = client.ApiClient(configuration)
        apps_v1 = client.AppsV1Api(api_client)

        # Fetch the deployments
        deployments = apps_v1.list_deployment_for_all_namespaces()
        deployment_list = [{"name": deployment.metadata.name, "namespace": deployment.metadata.namespace} for deployment in deployments.items]

        return jsonify(deployment_list)

    except ApiException as e:
        return jsonify({"error": f"API exception: {e.reason}"}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

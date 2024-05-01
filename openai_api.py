import openai, os, requests

openai.api_type = "azure"
# Azure OpenAI on your own data is only supported by the 2023-08-01-preview API version
openai.api_version = "2023-08-01-preview"

# Azure OpenAI setup
openai.api_base = "https://openai-tigeranalytics-105.openai.azure.com/" # Add your endpoint here
openai.api_key = os.getenv("OPENAI_API_KEY") # Add your OpenAI API key here
deployment_id = "gpt-35-turbo-16k" # Add your deployment ID here

# Azure AI Search setup
search_endpoint = "https://undefined.search.windows.net"; # Add your Azure AI Search endpoint here
search_key = os.getenv("SEARCH_KEY"); # Add your Azure AI Search admin key here
search_index_name = "undefined"; # Add your Azure AI Search index name here

def setup_byod(deployment_id: str) -> None:
    """Sets up the OpenAI Python SDK to use your own data for the chat endpoint.

    :param deployment_id: The deployment ID for the model to use with your own data.

    To remove this configuration, simply set openai.requestssession to None.
    """

    class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):

        def send(self, request, **kwargs):
            request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
            return super().send(request, **kwargs)

    session = requests.Session()

    # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
    session.mount(
        prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
        adapter=BringYourOwnDataAdapter()
    )

    openai.requestssession = session

setup_byod(deployment_id)


message_text = [{"role": "user", "content": "What are the differences between Azure Machine Learning and Azure AI services?"}]

completion = openai.ChatCompletion.create(
    messages=message_text,
    deployment_id=deployment_id,
    dataSources=[  # camelCase is intentional, as this is the format the API expects
      {
  "type": "AzureMLIndex",
  "parameters": {
    "projectResourceId": "/subscriptions/b89995c4-e911-46aa-92e8-532abee49348/resourceGroups/rg-thailand46ai/providers/Microsoft.MachineLearningServices/workspaces/ai-build-thailand46-v1",
    "name": "funny-rose-mq46j2zz0l",
    "version": "1",
    "queryType": "vectorSimpleHybrid",
    "inScope": true,
    "roleInformation": "You are an AI assistant that helps people find information.",
    "strictness": 3,
    "topNDocuments": 5,
    "endpoint": "'$search_endpoint'",
    "key": "'$search_key'",
    "indexName": "'$search_index'"
  }
}
    ],
    enhancements=undefined,
    temperature=0,
    top_p=1,
    max_tokens=800,
    stop=null,
    stream=true

)
print(completion)
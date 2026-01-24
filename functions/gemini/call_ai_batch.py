import json
from google.genai import types
import time

MODEL_ID = "gemini-3-flash-preview"

def prepare_and_upload_input_file(client):
  # Create a sample JSONL file.
  # The 'key' field is required for correlating inputs to outputs.

  requests_data = [
      {"key": "request_1", "request": {"contents": [{"parts": [{"text": "Explain how AI works in a few words"}]}]}},
      {"key": "request_2", "request": {"contents": [{"parts": [{"text": "Explain how quantum computing works in a few words"}]}]}}
  ]

  json_file_path = 'batch_requests.json'

  with open(json_file_path, 'w') as f:
      for req in requests_data:
          f.write(json.dumps(req) + '\n')

  # 2. Upload JSONL file to File API.
  print(f"Uploading file: {json_file_path}")
  uploaded_batch_requests = client.files.upload(
      file=json_file_path,
      config=types.UploadFileConfig(display_name='batch-input-file')
  )
  print(f"Uploaded file: {uploaded_batch_requests.name}")

  batch_job_from_file = client.batches.create(
      model=MODEL_ID,
      src=uploaded_batch_requests.name,
      config={
          'display_name': 'my-batch-job-from-file',
      }
  )
  print(f"Created batch job from file: {batch_job_from_file.name}")
  return batch_job_from_file.name
  
def monitor_job_status(client, job_name):
  print(f"Polling status for job: {job_name}")

  # Poll the job status until it's completed.
  while True:
      batch_job = client.batches.get(name=job_name)
      if batch_job.state.name in ('JOB_STATE_SUCCEEDED', 'JOB_STATE_FAILED', 'JOB_STATE_CANCELLED'):
          break
      print(f"Job not finished. Current state: {batch_job.state.name}. Waiting 30 seconds...")
      time.sleep(30)

  print(f"Job finished with state: {batch_job.state.name}")
  if batch_job.state.name == 'JOB_STATE_FAILED':
      print(f"Error: {batch_job.error}")
      
  return batch_job
     
def retrive_parse_results(client, batch_job):
  if batch_job.state.name == 'JOB_STATE_SUCCEEDED':
    # The output is in another file.
    result_file_name = batch_job.dest.file_name
    print(f"Results are in file: {result_file_name}")

    print("\nDownloading and parsing result file content...")
    file_content_bytes = client.files.download(file=result_file_name)
    file_content = file_content_bytes.decode('utf-8')

    # The result file is also a JSONL file. Parse and print each line.
    for line in file_content.splitlines():
      if line:
        parsed_response = json.loads(line)
        # Pretty-print the JSON for readability
        print(json.dumps(parsed_response, indent=2))
        print("-" * 20)
  else:
      print(f"Job did not succeed. Final state: {batch_job.state.name}")

def call_ai_batch(client):
  job_name = prepare_and_upload_input_file(client)
  #job_name = create_batch_job(client, uploaded_batch_requests)
  batch_job = monitor_job_status(client, job_name)
  retrive_parse_results(client, batch_job)
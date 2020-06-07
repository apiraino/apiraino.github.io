### A notebook. Because why not.

[apiraino.github.io](https://apiraino.github.io)

### Running the website on localhost with Zola

- `$ git clone https://github.com/apiraino/apiraino.github.io.git`
- `$ zola serve`
- Connect to `http://127.0.0.1:1111`

Github Action for deployment provided by: https://github.com/shalzz/zola-deploy-action

### Running the website on a local Docker container (**OLD**)

- Install Docker and Docker compose ([+1.24 version](https://docs.docker.com/compose/install))
- If it's the first time you run locally, create the local deployment files with: `docker run -v $(pwd):/site bretfisher/jekyll new . --force`
- Run the container using the compose file `docker-compose up`
- Connect to `http://localhost:8000`

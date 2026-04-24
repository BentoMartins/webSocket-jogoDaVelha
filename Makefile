.PHONY: setup run tunnel-lhr tunnel-serveo tunnel dev-lhr dev-serveo dev stop

setup:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt	

run:
	./venv/bin/python3 main.py

tunnel-lhr:
	ssh -R 80:localhost:8888 nokey@localhost.run -o StrictHostKeyChecking=no

tunnel-serveo:
	ssh -R velhia:80:localhost:8888 serveo.net -o StrictHostKeyChecking=no

tunnel: tunnel-serveo

dev-lhr:
	$(MAKE) run &
	$(MAKE) tunnel-lhr

dev-serveo:
	$(MAKE) run &
	$(MAKE) tunnel-serveo

dev: dev-serveo

stop:
	@lsof -ti :8888 | xargs kill -9 2>/dev/null && echo "Servidor encerrado." || echo "Nenhum servidor rodando."
	@pkill -f "ssh.*serveo.net" 2>/dev/null && echo "Túnel serveo encerrado." || echo "Nenhum túnel serveo ativo."
	@pkill -f "ssh.*localhost.run" 2>/dev/null && echo "Túnel lhr encerrado." || echo "Nenhum túnel lhr ativo."
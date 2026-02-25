help: ##@ (Default) Print listing of key targets with their descriptions
	@printf "\nUsage: make <command>\n"
	@grep -F -h "##@" $(MAKEFILE_LIST) | grep -F -v grep -F | sed -e 's/\\$$//' | awk 'BEGIN {FS = ":*[[:space:]]*##@[[:space:]]*"}; \
	{ \
		if($$2 == "") \
			pass; \
		else if($$0 ~ /^#/) \
			printf "%s\n", $$2; \
		else if($$1 == "") \
			printf "     %-20s%s\n", "", $$2; \
		else \
			printf "    \033[34m%-20s\033[0m %s\n", $$1, $$2; \
	}'
##@ ---------------------
##@ Molecular Polarisation
##@ ---------------------
pol_sublight: ##@ Sublight polarisation
	mamba run -n manimgl manimgl $(CURDIR)/Air_showers/Cherenkov_polarisation.py sublight --resolution 2000x2000

pol_light: ##@ Lightspeed polarisation 
	mamba run -n manimgl manimgl $(CURDIR)/Air_showers/Cherenkov_polarisation.py lightspeed --resolution 2000x2000

pol_superluminal: ##@ Superluminal polarisation 
	mamba run -n manimgl manimgl $(CURDIR)/Air_showers/Cherenkov_polarisation.py superluminal --resolution 2000x2000


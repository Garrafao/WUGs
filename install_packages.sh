# Install graph-tool
conda config --set auto_activate_base false
conda create --name wug -c conda-forge graph-tool # this should work only linux

# Install remaining main packages
#conda create --name wug
conda activate wug
conda install scikit-learn
conda install requests
conda install pandas
conda install networkx
conda install matplotlib

# Additional packages not available with conda
conda install pip
#python -m pip install mlrose # This may work again after the maintainers update their code
python -m pip install https://github.com/gkhayes/mlrose/archive/refs/heads/master.zip # use pip install --force-reinstall to ignore locally preinstalled versions
python -m pip install chinese_whispers
python -m pip install python-louvain
python -m pip install pyvis==0.1.9

# To validate your installation, consider now running this
bash -e test.sh

# Export environment
#conda env export > packages.yml

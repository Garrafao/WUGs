#conda clean --all -y
#conda update --all -y
#conda remove -n wug_wsbm1 --all -y

# Install graph-tool
conda config --set auto_activate_base false
conda create --name wug_wsbm1 -c conda-forge graph-tool -y # this should work only linux

# Install remaining main packages
#conda create --name wug
conda activate wug_wsbm1
conda install -y jupyter
conda install -y jupyterlab
conda install -y scikit-learn
conda install -y requests
conda install -y pandas
conda install -y networkx
conda install -y matplotlib
conda install -y pygraphviz 

# Additional packages not available with conda
conda install -y pip
#python -m pip install mlrose # This may work again after the maintainers update their code
python -m pip install https://github.com/gkhayes/mlrose/archive/refs/heads/master.zip # use pip install --force-reinstall to ignore locally preinstalled versions
python -m pip install chinese_whispers
python -m pip install python-louvain
python -m pip install pyvis==0.1.9

# To validate your installation, consider now running this
bash -e test.sh

# Export environment
#conda env export > packages.yml

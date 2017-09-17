# operation-goose
API detecting change and motion in surveillance footage. Built for Hack the North 2017.

# Setup
First, install Anaconda3 from online.
Then

```
conda update conda
conda create -n goose python=3.6 anaconda
source activate goose

conda uninstall numpy # sometimes needs to be reinstalled alongside tensorflow for darkflow to work
conda install tensorflow opencv

git clone https://github.com/ninkle/operation-goose
cd operation-goose
git submodule update --init --recursive

cd darkflow

pip install -e .

mkdir bin
cd bin
wget --no-check-certificate https://pjreddie.com/media/files/tiny-yolo-voc.weights

cd ..
cd cfg
wget --no-check-certificate https://pjreddie.com/media/files/tiny-yolo-voc.weights


cd ../..
``
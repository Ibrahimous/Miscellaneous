#Install homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

#add Homebrew to your PATH:
(echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> /home/charlou/.bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
#Install Homebrew's dependencies if you have sudo access:
sudo apt-get install build-essential

#We recommend that you install GCC:
brew install gcc

#Finally:
brew update

#New setup
brew install golang

#Existing setup
brew upgrade golang
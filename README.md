# Babyslam

This program is intended to let baby's slam away on the computer's keyboard
without being able to break software.

Be aware that babies slamming away at your keyboard could break hardware.

Needless to say, I'm not responsible for either (software or hardware breakage).

## Installation

	git clone git://github.com/karel1980/babyslam.git
	cd babyslam
	sudo pip install -r requirements.txt
	sudo python setup.py install

Install additinal sample imagery

	./install_samples.sh

## Running

Simply run:

	babyslam
	
## Usage

To quit, type 'babydodo'. This will always be visible in the top left corner, so no need to remember it.

## Configuration

You can let babyslam use custom images/animations.
To do so, run babyslam -c path/to/config.xml
To learn more, extract the samples from the samples directory





Legiscan API Scripts
======
These scripts use the [Legiscan API](https://legiscan.com/legiscan) to get bills from Arizona's legislature into a pure text
format. Others interested in doing the same but for other states need only modify the API call in the code.

You can then analyze the text for similarities to other legislation using the 
[Data Science for the Social Good's](https://dssg.uchicago.edu/) awsome tool to track
legislative plagiarism, [the Legislative Influence Detector](https://dssg.uchicago.edu/lid/)

Here's the GitHub repo for that: [LID](https://github.com/dssg/policy_diffusion)

These scripts are compatible with Python 3. If you're using Python 2, install Python 3 and follow [Kenneth Reitz's](https://github.com/kennethreitz)
excellent [tutorial](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to set up a virtual environment pointing to your
Python 3 install.

Once your Python 3 virtual environment is activated and you're inside the LegiscanApiScripts directory, 
run `pip install -r requirements.txt`

###Setup

1. Clone the repository to your machine: `git clone https://github.com/qstin/LegiScanApiScripts.git`
2. cd into the cloned directory.
3. Set up a virtual Python environment if needed.
4. Check everything is working by running `python leg-text-generator.py`
    This program is what writes the bills to text files in `~/path/to/LegiScanApiScripts/bills`. Be prepared for this to run for while.
5. You'll need to set up your environmental variables for the LID project's algorithm. To do that, type each of these commands into your terminal:

    ```
    unset PYTHONPATH
    export POLICY_DIFFUSION=/path/to/policy_diffusion
    export PYTHONPATH=${POLICY_DIFFUSION}/lid:${PYTHONPATH}
    export PYTHONPATH=${POLICY_DIFFUSION}/lid/etl:${PYTHONPATH}
    export PYTHONPATH=${POLICY_DIFFUSION}/lid/utils:${PYTHONPATH}
    export PYTHONPATH=${POLICY_DIFFUSION}/lid/evaluation:${PYTHONPATH}
    export PYTHONPATH=${POLICY_DIFFUSION}/scripts:${PYTHONPATH}
    ```
    
6. Once that's done and you've got your bills directory filled with text files, you can run the LID script.
    - This process takes forever, maybe up to six hours if you're running all of your bills through at once.

7. To run one bill at a time, enter this into your command line from the LID directory:
 
    ```
    cat sampleFile.txt | xargs -0 python LID/lid_script.py -text

    ```
8. To run all bills in the bill directory at once, run this:

    ```
    parallel "cat {} | xargs -0 python LID/lid_script.py -text > {.}.json" ::: data/bills/*.txt
    
    ```


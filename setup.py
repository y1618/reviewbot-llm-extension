from setuptools import setup, find_packages

setup(
    name='reviewbot-llm-extension',
    version='1.0.0',
    description='ReviewBot extension for LLM-based code reviews using OpenWebUI and llamacpp',
    author='ReviewBot LLM Extension',
    author_email='reviewbot-llm@example.com',
    url='https://github.com/y1618/reviewbot-llm-extension',
    packages=find_packages(),
    install_requires=[
        'requests',
        'llama-cpp-python',
    ],
    extras_require={
        'dev': [
            'reviewbot',
        ],
    },
    entry_points={
        'reviewbot.tools': [
            'llm = reviewbot_llm.llm_tool:LLMTool',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)

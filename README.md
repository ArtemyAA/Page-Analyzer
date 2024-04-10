### Hexlet tests and linter status

[![Actions Status](https://github.com/ArtemyAA/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ArtemyAA/python-project-83/actions)
[![Lint](https://github.com/ArtemyAA/python-project-83/actions/workflows/linter.yml/badge.svg)](https://github.com/ArtemyAA/python-project-83/actions/workflows/linter.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/20a2c19a2e5abf321796/maintainability)](https://codeclimate.com/github/ArtemyAA/python-project-83/maintainability)

### [Page Analyzer](https://python-project-83-w3lx.onrender.com/) – this is a site that analyzes input websites for SEO suitability

#### Installation

Clone the repository:

```git clone git@github.com:ArtemyAA/python-project-83.git```

#### Usage

1. Firstly, copy file `.env.sample` в `.env`

```cp .env.sample .env```
2. Fill '.env' file`s keys with needed information. You can see the example in
key`s definition
3. Install dependencies using bash script and also set the database

```make build```
4. Install dependencies with Poetry

```make pack-install```
5. Start the server:

```make start```

#### Now you can enter url in the browser on localhost and parse info from html page. :clap: :clap: :clap:

from flask import Flask, request, redirect, url_for, abort, render_template, session
from application.services.utils import now_time_iso


def convert_to_dict_machine(dict_v, new_v={}):
    dict_v.update(new_v)
    return dict_v

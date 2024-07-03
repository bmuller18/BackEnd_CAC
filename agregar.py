from flask import Flask, jsonify, render_template, request, redirect, url_for
import mysql.connector
from flask_cors import CORS
from config import MYSQL_CONFIG

def conectar():
    conexion = mysql.connector.connect(**MYSQL_CONFIG)
    return conexion

def desconectar(conexion):
    if conexion:
        conexion.close()



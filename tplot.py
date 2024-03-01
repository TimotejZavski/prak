
import json
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import math

def create_chart(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['blue', 'red']

    ax.bar(data['culmen_length_mm'], data['body_mass_g'], color=colors[int(data['sex'])])

    ax2 = fig.add_subplot(212)
    ax2.bar(data['flipper_length_mm'], data['body_mass_g'], color=colors[int(data['sex'])])

    x_position = 0
    y_position = 0

    for index, row in data.items():
        x_position += row['culmen_length_mm'] + 5
        y_position += row['body_mass_g'] + 5

    ax2.set_xlim(0, max(x_position, y_position))
    ax.set_ylim(0, max(x_position, y_position))

    ax.set_title('Penguin Culmen Length and Body Mass')
    ax2.set_title('Penguin Flipper Length and Body Mass')

    ax.set_xlabel('Culmen Length (mm)')
    ax.set_ylabel('Body Mass (g)')

    ax2.set_xlabel('Flipper Length (mm)')
    ax2.set_ylabel('Body Mass (g)')

    plt.xticks(rotation=45)
    plt.yticks()

    chart_width, chart_height = fig.get_size().split()
    font = ImageFont.truetype('arial.ttf', 16)
    plt.text(x_position - 20, y_position + 5, 'Culmen Length vs Body Mass', font=font, ha='center')
    plt.text(x_position + chart_width / 2, y_position + 5, 'Flipper Length vs Body Mass', font=font, ha='center')

    plt.savefig('/Users/timzav/Desktop/prak/static/images/chart1.png', bbox_inches='tight')

    plt.clf()
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ['blue', 'red']

    ax.plot(data['culmen_length_mm'], data['body_mass_g'], color=colors[int(data['sex'])], marker='o')

    ax2 = fig.add_subplot(212)
    ax2.plot(data['flipper_length_mm'], data['body_mass_g'], color=colors[int(data['sex'])], marker='s')

    plt.xlabel('Culmen Length (mm)')
    plt.ylabel('Body Mass (g)')

    plt.xticks()
    plt.yticks()

    chart_width, chart_height = fig.get_size().split()
    font = ImageFont.truetype('arial.ttf', 16)
    plt.text(x_position - 20, y_position + 5, 'Culmen Length vs Body Mass', font=font, ha='center')
    plt.text(x_position + chart_width / 2, y_position + 5, 'Flipper Length vs Body Mass', font=font, ha='center')

    plt.savefig('/Users/timzav/Desktop/prak/static/images/chart2.png', bbox_inches='tight')

    plt.clf()

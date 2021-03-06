from .context import lux
import pytest
import pandas as pd
import numpy as np
from lux.interestingness.interestingness import interestingness

# The following test cases are labelled for vis with <Ndim, Nmsr, Nfilter>
def test_interestingness_1_0_0():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    
    df.set_intent([lux.Clause(attribute = "Origin")])
    df._repr_html_()
    #check that top recommended enhance graph score is not none and that ordering makes intuitive sense
    assert interestingness(df.recommendation['Enhance'][0],df) != None
    rank1 = -1
    rank2 = -1
    rank3 = -1
    for f in range(0, len(df.recommendation['Enhance'])):
        vis = df.recommendation['Enhance'][f]
        if vis.get_attr_by_channel("x")[0].attribute == 'Displacement':
            rank1 = f
        if vis.get_attr_by_channel("x")[0].attribute == 'Weight':
            rank2 = f
        if vis.get_attr_by_channel("x")[0].attribute == 'Acceleration':
            rank3 = f
    assert rank1 < rank2 and rank1 < rank3 and rank2 < rank3

    #check that top recommended filter graph score is not none and that ordering makes intuitive sense
    assert interestingness(df.recommendation['Filter'][0],df) != None
    rank1 = -1
    rank2 = -1
    rank3 = -1
    for f in range(0, len(df.recommendation['Filter'])):
        vis = df.recommendation['Filter'][f]
        if len(vis.get_attr_by_attr_name("Cylinders"))>0:
            if int(vis._inferred_intent[2].value) == 8:
                rank1 = f
            if int(vis._inferred_intent[2].value) == 6:
                rank2 = f
        if '1972' in str(df.recommendation['Filter'][f]._inferred_intent[2].value):
            rank3 = f
    assert rank1 < rank2 and rank1 < rank3 and rank2 < rank3
def test_interestingness_1_0_1():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')

    df.set_intent([lux.Clause(attribute = "Origin", filter_op="=",value="USA"),lux.Clause(attribute = "Cylinders")])
    df._repr_html_()
    assert df.current_vis[0].score == 0

def test_interestingness_0_1_0():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')

    df.set_intent([lux.Clause(attribute = "Horsepower")])
    df._repr_html_()
    #check that top recommended enhance graph score is not none and that ordering makes intuitive sense
    assert interestingness(df.recommendation['Enhance'][0],df) != None
    rank1 = -1
    rank2 = -1
    rank3 = -1
    for f in range(0, len(df.recommendation['Enhance'])):
        if df.recommendation['Enhance'][f].mark == 'scatter' and df.recommendation['Enhance'][f]._inferred_intent[1].attribute == 'Weight':
            rank1 = f
        if df.recommendation['Enhance'][f].mark == 'scatter' and df.recommendation['Enhance'][f]._inferred_intent[1].attribute == 'Acceleration':
            rank2 = f
        if df.recommendation['Enhance'][f].mark == 'line' and df.recommendation['Enhance'][f]._inferred_intent[0].attribute == 'Year':
            rank3 = f
    assert rank1 < rank2 and rank1 < rank3 and rank2 < rank3

    #check that top recommended filter graph score is not none and that ordering makes intuitive sense
    assert interestingness(df.recommendation['Filter'][0],df) != None
    rank1 = -1
    rank2 = -1
    rank3 = -1
    for f in range(0, len(df.recommendation['Filter'])):
        if df.recommendation['Filter'][f]._inferred_intent[2].value == 4:
            rank1 = f
        if str(df.recommendation['Filter'][f]._inferred_intent[2].value) == "Europe":
            rank2 = f
        if '1971' in str(df.recommendation['Filter'][f]._inferred_intent[2].value):
            rank3 = f
    assert rank1 < rank2 and rank1 < rank3 and rank2 < rank3


def test_interestingness_0_1_1():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')
    
    df.set_intent([lux.Clause(attribute = "Origin", filter_op="=",value="?"),lux.Clause(attribute = "MilesPerGal")])
    df._repr_html_()
    assert interestingness(df.recommendation['Current Vis'][0],df) != None
    assert str(df.recommendation['Current Vis'][0]._inferred_intent[2].value) == 'USA'

def test_interestingness_1_1_0():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')

    df.set_intent([lux.Clause(attribute = "Horsepower"),lux.Clause(attribute = "Year")])
    df._repr_html_()
    #check that top recommended Enhance graph score is not none (all graphs here have same score)
    assert interestingness(df.recommendation['Enhance'][0],df) != None

    #check that top recommended filter graph score is not none and that ordering makes intuitive sense
    assert interestingness(df.recommendation['Filter'][0],df) != None
    rank1 = -1
    rank2 = -1
    rank3 = -1
    for f in range(0, len(df.recommendation['Filter'])):
        vis = df.recommendation['Filter'][f]
        if len(vis.get_attr_by_attr_name("Cylinders"))>0:
            if int(vis._inferred_intent[2].value) == 6:
                rank1 = f
            if int(vis._inferred_intent[2].value) == 5:
                rank3 = f
        if len(vis.get_attr_by_attr_name("Origin"))>0:
            if str(vis._inferred_intent[2].value) == "Europe":
                rank2 = f
    assert rank1 < rank2 and rank1 < rank3 and rank2 < rank3

    #check that top recommended generalize graph score is not none
    assert interestingness(df.recommendation['Filter'][0],df) != None

def test_interestingness_1_1_1():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')

    df.set_intent([lux.Clause(attribute = "Horsepower"), lux.Clause(attribute = "Origin", filter_op="=",value = "USA", bin_size=20)])
    df._repr_html_()
    #check that top recommended Enhance graph score is not none and that ordering makes intuitive sense
    assert interestingness(df.recommendation['Enhance'][0],df) != None
    rank1 = -1
    rank2 = -1
    rank3 = -1
    for f in range(0, len(df.recommendation['Enhance'])):
        if str(df.recommendation['Enhance'][f]._inferred_intent[2].value) == "USA" and str(df.recommendation['Enhance'][f]._inferred_intent[1].attribute) == 'Cylinders':
            rank1 = f
        if str(df.recommendation['Enhance'][f]._inferred_intent[2].value) == "USA" and str(df.recommendation['Enhance'][f]._inferred_intent[1].attribute) == 'Weight':
            rank2 = f
        if str(df.recommendation['Enhance'][f]._inferred_intent[2].value) == "USA" and str(df.recommendation['Enhance'][f]._inferred_intent[1].attribute) == 'Horsepower':
            rank3 = f
    assert rank1 < rank2 and rank1 < rank3 and rank2 < rank3

    #check for top recommended Filter graph score is not none
    assert interestingness(df.recommendation['Filter'][0],df) != None

def test_interestingness_1_2_0():
    from lux.vis.Vis import Vis
    from lux.vis.Vis import Clause
    from lux.interestingness.interestingness import interestingness

    df = pd.read_csv("lux/data/car.csv")
    y_clause = Clause(attribute = "Name", channel = "y")
    color_clause = Clause(attribute = 'Cylinders', channel = "color")

    new_vis = Vis([y_clause, color_clause])
    new_vis.refresh_source(df)
    new_vis
    #assert(len(new_vis.data)==color_cardinality*group_by_cardinality)

    assert(interestingness(new_vis, df)<0.01)

def test_interestingness_0_2_0():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')

    df.set_intent([lux.Clause(attribute = "Horsepower"),lux.Clause(attribute = "Acceleration")])
    df._repr_html_()
    #check that top recommended enhance graph score is not none and that ordering makes intuitive sense
    assert interestingness(df.recommendation['Enhance'][0],df) != None
    rank1 = -1
    rank2 = -1
    rank3 = -1
    for f in range(0, len(df.recommendation['Enhance'])):
        if str(df.recommendation['Enhance'][f]._inferred_intent[2].attribute) == "Origin" and str(df.recommendation['Enhance'][f].mark) == 'scatter':
            rank1 = f
        if str(df.recommendation['Enhance'][f]._inferred_intent[2].attribute) == "Displacement" and str(df.recommendation['Enhance'][f].mark) == 'scatter':
            rank2 = f
        if str(df.recommendation['Enhance'][f]._inferred_intent[2].attribute) == "Year" and str(df.recommendation['Enhance'][f].mark) == 'scatter':
            rank3 = f
    assert rank1 < rank2 and rank1 < rank3 and rank2 < rank3

    #check that top recommended filter graph score is not none and that ordering makes intuitive sense
    assert interestingness(df.recommendation['Filter'][0],df) != None
    rank1 = -1
    rank2 = -1
    rank3 = -1
    for f in range(0, len(df.recommendation['Filter'])):
        if '1973' in str(df.recommendation['Filter'][f]._inferred_intent[2].value):
            rank1 = f
        if '1976' in str(df.recommendation['Filter'][f]._inferred_intent[2].value):
            rank2 = f
        if str(df.recommendation['Filter'][f]._inferred_intent[2].value) == "Europe":
            rank3 = f
    assert rank1 < rank2 and rank1 < rank3 and rank2 < rank3

    #check that top recommended Generalize graph score is not none
    assert interestingness(df.recommendation['Generalize'][0],df) != None


def test_interestingness_0_2_1():
    df = pd.read_csv("lux/data/car.csv")
    df["Year"] = pd.to_datetime(df["Year"], format='%Y')

    df.set_intent([lux.Clause(attribute = "Horsepower"),lux.Clause(attribute = "MilesPerGal"),lux.Clause(attribute = "Acceleration", filter_op=">",value = 10)])
    df._repr_html_()
    #check that top recommended Generalize graph score is not none
    assert interestingness(df.recommendation['Generalize'][0],df) != None
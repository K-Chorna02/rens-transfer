# PIE CHART – TtoR Distribution
#This file is just a list of functions which generate graphs.
#They are used in app restart to regenerate

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os


def ttor_distribution(df):

    plot_df = (
        df["TtoR"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    plot_df.columns = ["TtoR", "Organisations"]

    fig = px.bar(
        plot_df,
        x="TtoR",
        y="Organisations",
        text="Organisations",
        title="Distribution of TtoR",
        color_discrete_sequence=["#51A9DB"]
    )

    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        xaxis_title="TtoR",
        yaxis_title="Number of Organisations",
        bargap=0.2,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A")
    )
    fig.update_xaxes(showline=True, linecolor="#020A0A")
    fig.update_yaxes(rangemode="tozero", showline=True, linecolor="#020A0A")

    return fig

def organisations_ttor_variety_heatmap(df: pd.DataFrame):
    plot_df = df.dropna(subset=["TtoR", "Variety"]).copy()
    heatmap_df = (
        plot_df.groupby(["TtoR", "Variety"])
        .size()
        .reset_index(name="Organisations")
        .pivot(index="TtoR", columns="Variety", values="Organisations")
        .fillna(0)
    )
    # ensure TtoR order
    heatmap_df = heatmap_df.reindex(index=[1, 2, 3, 4, 5])
    fig = px.imshow(
        heatmap_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        title="Organisations by TtoR and Variety"
    )
    fig.update_layout(
        xaxis_title="Variety",
        yaxis_title="TtoR",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=0, r=0, t=60, b=0),
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="#020A0A", width=1),
                fillcolor="rgba(0,0,0,0)",
            )
        ],
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        coloraxis_showscale=False
    )
    fig.update_xaxes(showline=True, linecolor="#020A0A")
    fig.update_yaxes(showline=True, linecolor="#020A0A")
    fig.update_traces(
        xgap=2,
        ygap=2,
        hovertemplate="Variety: %{x}<br>TtoR: %{y}<br>Organisations: %{z}<extra></extra>"
    )
    return fig

def org_priority_counts(df):

    priority_cols = ["EQ", "RJ", "CU", "CJ", "SO", "SJ", "CE", "SC"]

    long_df = (
        df[["Organisation"] + priority_cols]
        .melt(id_vars=["Organisation"], var_name="Priority", value_name="Flag")
    )

    long_df = long_df[long_df["Flag"] == True]

    plot_df = (
        long_df["Priority"]
        .value_counts()
        .reset_index()
    )

    plot_df.columns = ["Priority", "Organisations"]

    fig = px.bar(
        plot_df,
        x="Priority",
        y="Organisations",
        text="Organisations",
        title="Organisation Priorities Distribution",
        color="Organisations",
        color_continuous_scale=["#EBEBEE", "#51A9DB", "#31B7BC", "#FFCC00", "#E30613", "#020A0A"]
    )

    fig.update_coloraxes(showscale=False)
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        xaxis_title="Priority",
        yaxis_title="Number of Organisations",
        bargap=0.2,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A")
    )
    fig.update_xaxes(showline=True, linecolor="#020A0A")
    fig.update_yaxes(rangemode="tozero", showline=True, linecolor="#020A0A")

    return fig

def priority_ttor_heatmap(df):
    priority_cols = ["EQ", "RJ", "CU", "CJ", "SO", "SJ", "CE", "SC"]

    long_df = (
        df[["TtoR"] + priority_cols]
        .melt(id_vars=["TtoR"], var_name="Priority", value_name="Flag")
    )

    long_df = long_df[long_df["Flag"] == True]

    heatmap_df = (
        long_df.groupby(["TtoR", "Priority"])
        .size()
        .reset_index(name="Count")
        .pivot(index="TtoR", columns="Priority", values="Count")
        .fillna(0)
    )

    fig = px.imshow(
        heatmap_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        title="Priority vs TtoR"
    )

    fig.update_layout(
        xaxis_title="Priority",
        yaxis_title="TtoR",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=0, r=0, t=60, b=0),
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="#020A0A", width=1),
                fillcolor="rgba(0,0,0,0)",
            )
        ],
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        coloraxis_showscale=False
    )
    fig.update_xaxes(showline=True, linecolor="#020A0A")
    fig.update_yaxes(showline=True, linecolor="#020A0A")
    fig.update_traces(
        xgap=2,
        ygap=2,
        hovertemplate="Priority: %{x}<br>TtoR: %{y}<br>Count: %{z}<extra></extra>"
    )

    return fig

'''
def visualpie(df: pd.DataFrame) -> go.Figure:
    counts = df.groupby('TtoR')['Organisation'].count().reset_index()
    counts.columns = ['TtoR', 'Organisation_Count']

    fig = go.Figure(
        go.Pie(
            labels=counts['TtoR'],
            values=counts['Organisation_Count'],
            hoverinfo='label+percent'
        )
    )
    fig.update_layout(title="Number of Organisations by TtoR")
    return fig


# HEATMAP – TtoR × Variety
def visualheatmap(df: pd.DataFrame) -> go.Figure:
    counts = df.groupby(['TtoR', 'Variety'])['Organisation'].count().reset_index()
    table = counts.pivot(index='TtoR', columns='Variety', values='Organisation').fillna(0)

    fig = go.Figure(
        go.Heatmap(
            z=table.values,
            x=table.columns,
            y=table.index,
            colorscale='Blues'
        )
    )
    fig.update_layout(title='Organisations by TtoR & Variety')
    return fig


# HEATMAP – TtoR × Area of Operation
def visualheatmap2(df: pd.DataFrame) -> go.Figure:
    counts = df.groupby(['TtoR', 'Area of Operation'])['Organisation'].count().reset_index()
    table = counts.pivot(index='TtoR', columns='Area of Operation', values='Organisation').fillna(0)

    fig = go.Figure(
        go.Heatmap(
            z=table.values,
            x=table.columns,
            y=table.index,
            colorscale='Blues'
        )
    )
    fig.update_layout(title='Organisations by TtoR & Area of Operation')
    return fig


# STACKED BAR – Regularity × Focus
def visualstackbar(df: pd.DataFrame) -> go.Figure:
    counts = df.groupby(['Regularity', 'Focus'])['Organisation'].count().reset_index()
    
    fig = go.Figure()
    for focus in counts['Focus'].unique():
        sub = counts[counts['Focus'] == focus]
        fig.add_trace(go.Bar(x=sub['Regularity'], y=sub['Organisation'], name=focus))

    fig.update_layout(title="Organisations vs Regularity (Focus)", barmode='stack')
    return fig


# STACKED BAR – Regularity × Type
def visualstackbar2(df: pd.DataFrame) -> go.Figure:
    counts = df.groupby(['Regularity', 'Type'])['Organisation'].count().reset_index()
    
    fig = go.Figure()
    for t in counts['Type'].unique():
        sub = counts[counts['Type'] == t]
        fig.add_trace(go.Bar(x=sub['Regularity'], y=sub['Organisation'], name=t))

    fig.update_layout(title="Organisations vs Regularity (Type)", barmode='stack')
    return fig


# BAR CHART – Regularity Count
def visualbar(df: pd.DataFrame) -> go.Figure:
    counts = df.groupby('Regularity')['Organisation'].count().reset_index()

    fig = go.Figure(go.Bar(x=counts['Regularity'], y=counts['Organisation']))
    fig.update_layout(title="Organisations by Regularity")
    return fig


# HEATMAP – Priorities × Regularity
def visualheatmap3(df: pd.DataFrame) -> go.Figure:
    cols = ["Organisation", "Regularity", "EQ", "RJ", "CU", "CJ", "SO", "SJ", "CE", "SC"]

    df_bin = df[cols].copy()
    priority_cols = df_bin.columns[2:]
    df_bin[priority_cols] = df_bin[priority_cols].eq("Y").astype(int)

    counts = df_bin.groupby("Regularity")[priority_cols].sum()

    fig = go.Figure(
        go.Heatmap(
            z=counts.values,
            x=counts.columns,
            y=counts.index,
            colorscale='Blues'
        )
    )
    fig.update_layout(title="Priorities by Regularity")
    return fig


# HEATMAP – Priorities × Variety
def visualheatmap4(df: pd.DataFrame) -> go.Figure:
    cols = ["Organisation", "Variety", "EQ", "RJ", "CU", "CJ", "SO", "SJ", "CE", "SC"]

    df_bin = df[cols].copy()
    priority_cols = df_bin.columns[2:]
    df_bin[priority_cols] = df_bin[priority_cols].eq("Y").astype(int)

    counts = df_bin.groupby("Variety")[priority_cols].sum()

    fig = go.Figure(
        go.Heatmap(
            z=counts.values,
            x=counts.columns,
            y=counts.index,
            colorscale='Blues'
        )
    )
    fig.update_layout(title="Priorities by Variety")
    return fig
    '''
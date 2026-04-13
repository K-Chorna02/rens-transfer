#This file is just a list of functions which generate graphs.
#They are used in app restart to regenerate

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import numpy as np

def activities_over_time(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    plot_df = (
        df.dropna(subset=["Date"])
        .assign(Month=lambda x: x["Date"].dt.to_period("M"))
        .groupby("Month")
        .size()
        .rename("Activities")
        .reset_index()
    )
    # keeps chronological order
    plot_df = plot_df.sort_values("Month")
    # make labels display nicely
    plot_df["MonthLabel"] = plot_df["Month"].dt.strftime("%b %y")

    fig = px.bar(
    plot_df,
    x="MonthLabel",
    y="Activities",
    title="Activities Over Time (Monthly)",
    text="Activities",
    color_discrete_sequence=["#51A9DB"]  # brand blue

)

    fig.update_traces(textposition="outside", cliponaxis=False)

    fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Number of Activities",
    bargap=0.2,
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    margin=dict(l=40, r=40, t=60, b=40),
    font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
    coloraxis_showscale=False  # 👈 hides colour legend (important)
)

    fig.update_xaxes(tickangle=45, showline=True, linecolor="#020A0A")
    fig.update_yaxes(rangemode="tozero", showline=True, linecolor="#020A0A")
    return fig

def activities_heatmap_normalized(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    plot_df = (
        df.dropna(subset=["Date", "Workstreams"])
        .assign(Month=lambda x: x["Date"].dt.to_period("M"))
        .groupby(["Workstreams", "Month"])
        .size()
        .reset_index(name="Activities")
    )
    # keep month chronological
    plot_df["Month"] = plot_df["Month"].dt.to_timestamp()

    heatmap_df = plot_df.pivot(
        index="Workstreams",
        columns="Month",
        values="Activities"
    ).fillna(0)
    # sort rows by total activity
    heatmap_df = heatmap_df.loc[
        heatmap_df.sum(axis=1).sort_values(ascending=False).index
    ]
    # sort columns by month
    heatmap_df = heatmap_df.sort_index(axis=1)
    # keep raw counts for labels
    raw_counts = heatmap_df.copy()
    # normalize each row to 0-1
    normalized_df = heatmap_df.div(heatmap_df.max(axis=1).replace(0, 1), axis=0)
    # display-friendly month labels
    month_labels = normalized_df.columns.strftime("%b %y")
    normalized_df.columns = month_labels
    raw_counts.columns = month_labels
    fig = px.imshow(
        normalized_df,
        text_auto=False,
        aspect="auto",
        color_continuous_scale="Blues",
        title="Activities by Workstream and Month "
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Workstream",
        xaxis_tickangle=45,
        coloraxis_showscale=False,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=0, r=0, t=60, b=0),
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
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
        ]
    )
    fig.update_xaxes(showline=True, linecolor="#020A0A")
    fig.update_yaxes(showline=True, linecolor="#020A0A")
    fig.update_traces(
        xgap=2,
        ygap=2,
        text=raw_counts.values,
        texttemplate="%{text}",
        hovertemplate="Month: %{x}<br>Workstream: %{y}<br>Activities: %{text}<extra></extra>"
    )
    return fig

def activities_by_scale(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    plot_df = (
        df["Scale"]
        .value_counts()
        .reset_index()
    )
    plot_df.columns = ["Scale", "Activities"]

    fig = px.bar(
        plot_df,
        x="Scale",
        y="Activities",
        text="Activities",
        title="Activities by Scale",
        color_discrete_sequence=["#51A9DB"]
    )

    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        xaxis_title="Scale",
        yaxis_title="Number of Activities",
        bargap=0.2,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        coloraxis_showscale=False
    )
    fig.update_xaxes(tickangle=0, showline=True, linecolor="#020A0A")
    fig.update_yaxes(rangemode="tozero", showline=True, linecolor="#020A0A")

    return fig

def activities_by_engagement(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    plot_df = (
        df["Engagement"]
        .value_counts()
        .reset_index()
    )

    plot_df.columns = ["Engagement", "Activities"]
    fig = px.bar(
        plot_df,
        x="Engagement",
        y="Activities",
        text="Activities",
        title="Activities by Engagement Type",
        color_discrete_sequence=["#51A9DB"]
    )

    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        xaxis_title="Engagement",
        yaxis_title="Number of Activities",
        bargap=0.2,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        coloraxis_showscale=False
    )
    fig.update_xaxes(tickangle=0, showline=True, linecolor="#020A0A")
    fig.update_yaxes(rangemode="tozero", showline=True, linecolor="#020A0A")

    return fig

def activities_by_output(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    plot_df = (
        df["Output"]
        .value_counts()
        .reset_index()
    )

    plot_df.columns = ["Output", "Activities"]

    fig = px.bar(
        plot_df,
        x="Output",
        y="Activities",
        text="Activities",
        title="Activities by Output",
        color_discrete_sequence=["#51A9DB"]
    )

    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        xaxis_title="Output",
        yaxis_title="Number of Activities",
        bargap=0.2,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        coloraxis_showscale=False
    )
    fig.update_xaxes(tickangle=0, showline=True, linecolor="#020A0A")
    fig.update_yaxes(rangemode="tozero", showline=True, linecolor="#020A0A")

    return fig

def scale_engagement_heatmap(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    heatmap_df = (
        df.groupby(["Scale", "Engagement"])
        .size()
        .reset_index(name="Activities")
        .pivot(index="Scale", columns="Engagement", values="Activities")
        .fillna(0)
    )

    fig = px.imshow(
        heatmap_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        title="Scale vs Engagement"
    )

    fig.update_layout(
        xaxis_title="Engagement",
        yaxis_title="Scale",
        coloraxis_showscale=False,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=0, r=0, t=60, b=0),
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
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
        ]
    )
    fig.update_xaxes(showline=True, linecolor="#020A0A")
    fig.update_yaxes(showline=True, linecolor="#020A0A")
    fig.update_traces(
        xgap=2,
        ygap=2,
        hovertemplate="Engagement: %{x}<br>Scale: %{y}<br>Activities: %{z}<extra></extra>"
    )

    return fig

def engagement_output_heatmap(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    heatmap_df = (
        df.groupby(["Engagement", "Output"])
        .size()
        .reset_index(name="Activities")
        .pivot(index="Output", columns="Engagement", values="Activities")
        .fillna(0)
    )

    fig = px.imshow(
        heatmap_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        title="Engagement vs Output"
    )

    fig.update_layout(
        xaxis_title="Engagement",
        yaxis_title="Output",
        coloraxis_showscale=False,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=0, r=0, t=60, b=0),
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
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
        ]
    )
    fig.update_xaxes(showline=True, linecolor="#020A0A")
    fig.update_yaxes(showline=True, linecolor="#020A0A")
    fig.update_traces(
        xgap=2,
        ygap=2,
        hovertemplate="Engagement: %{x}<br>Output: %{y}<br>Activities: %{z}<extra></extra>"
    )

    return fig

def engagement_output_scale_bubble(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Engagement"] = df["Engagement"].replace({
        "Presentation": "M", "Meaningful": "M", "Nominal": "N", "Recruitment": "R"
    })
    df["Output"] = df["Output"].replace({
        "Unknown": "U", "Tangential": "T", "Meaningful": "M"
    })
    plot_df = (
        df.dropna(subset=["Engagement", "Output", "Scale"])
        .groupby(["Engagement", "Output", "Scale"])
        .size()
        .reset_index(name="Activities")
    )

    scale_order = ["Small", "Medium", "Large"]
    output_order = ["M", "T", "U"]

    fig = px.scatter(
        plot_df,
        x="Engagement",
        y="Output",
        size="Activities",
        color="Scale",
        facet_col="Scale",
        category_orders={"Scale": scale_order, "Output": output_order},
        size_max=45,
        title="Activities by Engagement and Output, Faceted by Scale",
    )

    fig.update_traces(
        marker=dict(line=dict(width=1, color="black")),
        opacity=0.8,
    )

    fig.update_xaxes(tickangle=0, title_text="", showline=True, linecolor="#AABBCC", mirror=True, linewidth=1.5)

    fig.update_yaxes(title_text="Output", ticklabelstandoff=15, showline=True, linecolor="#AABBCC", mirror=True, linewidth=1.5)

    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    fig.update_layout(
        showlegend=False,
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        plot_bgcolor="#EEF2F7",
        paper_bgcolor="#ffffff",
        margin=dict(l=80, r=40, t=60, b=82),
    )
    fig.add_annotation(
        text="<b>M</b> = Meaningful &nbsp;&nbsp;|&nbsp;&nbsp; <b>N</b> = Nominal &nbsp;&nbsp;|&nbsp;&nbsp; <b>R</b> = Recruitment",
        xref="paper", yref="paper",
        x=0.5, y=-0.16,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=11, color="#020A0A"),
        align="center",
    )
    fig.add_annotation(
        text="<b>U</b> = Unknown &nbsp;&nbsp;|&nbsp;&nbsp; <b>T</b> = Tangential &nbsp;&nbsp;|&nbsp;&nbsp; <b>M</b> = Meaningful",
        xref="paper", yref="paper",
        x=0.5, y=-0.24,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=11, color="#020A0A"),
        align="center",
    )
    fig.add_annotation(
        text="Engagement",
        xref="paper", yref="paper",
        x=0.5, y=-0.34,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        align="center",
    )
    fig.layout.yaxis2.title.text = ""
    fig.layout.yaxis3.title.text = ""

    return fig

def organisation_workstream_sankey(df, top_n=10):
    plot_df = df.dropna(subset=["Organisation", "Workstreams"]).copy()

    # Top organisations by activity count
    top_orgs = (
        plot_df["Organisation"]
        .value_counts()
        .head(top_n)
        .index
        .tolist()
    )

    # Group smaller orgs into "Other Organisations"
    plot_df["OrganisationGrouped"] = plot_df["Organisation"].where(
        plot_df["Organisation"].isin(top_orgs),
        "Other Organisations"
    )

    links_df = (
        plot_df.groupby(["OrganisationGrouped", "Workstreams"])
        .size()
        .reset_index(name="Value")
        .sort_values("Value", ascending=False)
    )

    orgs = links_df["OrganisationGrouped"].unique().tolist()
    workstreams = links_df["Workstreams"].unique().tolist()

    labels = orgs + workstreams
    label_to_idx = {label: i for i, label in enumerate(labels)}

    sources = links_df["OrganisationGrouped"].map(label_to_idx).tolist()
    targets = links_df["Workstreams"].map(label_to_idx).tolist()
    values = links_df["Value"].tolist()

    # Node colors
    org_color = "rgba(120,120,120,0.85)"
    workstream_palette = [
        "rgba(31,119,180,0.85)",
        "rgba(255,127,14,0.85)",
        "rgba(44,160,44,0.85)",
        "rgba(214,39,40,0.85)",
        "rgba(148,103,189,0.85)",
        "rgba(140,86,75,0.85)",
        "rgba(227,119,194,0.85)",
        "rgba(127,127,127,0.85)",
        "rgba(188,189,34,0.85)",
        "rgba(23,190,207,0.85)",
    ]

    node_colors = []
    for label in labels:
        if label in orgs:
            node_colors.append(org_color)
        else:
            idx = workstreams.index(label) % len(workstream_palette)
            node_colors.append(workstream_palette[idx])

    # Link colors follow target workstream color, but lighter
    link_colors = []
    for target_idx in targets:
        rgba = node_colors[target_idx]
        link_colors.append(rgba.replace("0.85", "0.35"))

    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=22,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=labels,
                    color=node_colors,
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values,
                    color=link_colors,
                ),
            )
        ]
    )

    fig.update_layout(
        title_text=f"Organisation to Workstream Flow (Top {top_n} + Other)",
        font_size=11,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
    )
    fig.update_xaxes(showline=True, linecolor="#020A0A", mirror=True)
    fig.update_yaxes(showline=True, linecolor="#020A0A", mirror=True)
    # Removed the rectangle border around the figure.

    return fig

def access_pie(df):
    df = df[df["Location"] == "The Other Place"].copy()
    df["Access"] = df["Access"].replace({"Open": "Public"})

    access_counts = df['Access'].value_counts().reset_index()
    access_counts.columns = ['Access', 'Count']

    fig_access = px.pie(
        access_counts,
        names='Access',
        values='Count',
        title='Access Proportion: The Other Place Activities',
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.0
    )

    fig_access.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
    )

    return fig_access


def meetings_engagement_output_bubble(df):
    df = df[df["Activity Type"] == "Meeting"].copy()
    df["Engagement"] = df["Engagement"].replace({
        "Presentation": "M", "Meaningful": "M", "Nominal": "N", "Recruitment": "R"
    })
    df["Output"] = df["Output"].replace({
        "Unknown": "U", "Tangential": "T", "Meaningful": "M"
    })
    plot_df = (
        df.dropna(subset=["Engagement", "Output", "Scale"])
        .groupby(["Engagement", "Output", "Scale"])
        .size()
        .reset_index(name="Activities")
    )
    scale_order = ["Small", "Medium", "Large"]
    output_order = ["M", "T", "U"]
    fig = px.scatter(
        plot_df, x="Engagement", y="Output", size="Activities",
        color="Scale", facet_col="Scale",
        category_orders={"Scale": scale_order, "Output": output_order},
        size_max=45,
        title="Meetings: Engagement vs Output by Scale",
    )
    fig.update_traces(marker=dict(line=dict(width=1, color="black")), opacity=0.8)
    fig.update_xaxes(tickangle=0, title_text="", showline=True, linecolor="#AABBCC", mirror=True, linewidth=1.5)
    fig.update_yaxes(title_text="Output", ticklabelstandoff=15, showline=True, linecolor="#AABBCC", mirror=True, linewidth=1.5)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(
        showlegend=False,
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        plot_bgcolor="#EEF2F7",
        paper_bgcolor="#ffffff",
        margin=dict(l=80, r=40, t=60, b=82),
    )
    fig.add_annotation(
        text="<b>M</b> = Meaningful &nbsp;&nbsp;|&nbsp;&nbsp; <b>N</b> = Nominal &nbsp;&nbsp;|&nbsp;&nbsp; <b>R</b> = Recruitment",
        xref="paper", yref="paper",
        x=0.5, y=-0.16,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=11, color="#020A0A"),
        align="center",
    )
    fig.add_annotation(
        text="<b>U</b> = Unknown &nbsp;&nbsp;|&nbsp;&nbsp; <b>T</b> = Tangential &nbsp;&nbsp;|&nbsp;&nbsp; <b>M</b> = Meaningful",
        xref="paper", yref="paper",
        x=0.5, y=-0.24,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=11, color="#020A0A"),
        align="center",
    )
    fig.add_annotation(
        text="Engagement",
        xref="paper", yref="paper",
        x=0.5, y=-0.34,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        align="center",
    )
    fig.layout.yaxis2.title.text = ""
    fig.layout.yaxis3.title.text = ""
    return fig


def events_engagement_output_bubble(df):
    df = df[df["Activity Type"] == "Event"].copy()
    df["Engagement"] = df["Engagement"].replace({
        "Presentation": "M", "Meaningful": "M", "Nominal": "N", "Recruitment": "R"
    })
    df["Output"] = df["Output"].replace({
        "Unknown": "U", "Tangential": "T", "Meaningful": "M"
    })
    plot_df = (
        df.dropna(subset=["Engagement", "Output", "Scale"])
        .groupby(["Engagement", "Output", "Scale"])
        .size()
        .reset_index(name="Activities")
    )
    scale_order = ["Small", "Medium", "Large"]
    output_order = ["M", "T", "U"]
    fig = px.scatter(
        plot_df, x="Engagement", y="Output", size="Activities",
        color="Scale", facet_col="Scale",
        category_orders={"Scale": scale_order, "Output": output_order},
        size_max=45,
        title="Events: Engagement vs Output by Scale",
    )
    fig.update_traces(marker=dict(line=dict(width=1, color="black")), opacity=0.8)
    fig.update_xaxes(tickangle=0, title_text="", showline=True, linecolor="#AABBCC", mirror=True, linewidth=1.5)
    fig.update_yaxes(title_text="Output", ticklabelstandoff=15, showline=True, linecolor="#AABBCC", mirror=True, linewidth=1.5)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(
        showlegend=False,
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        plot_bgcolor="#EEF2F7",
        paper_bgcolor="#ffffff",
        margin=dict(l=80, r=40, t=60, b=82),
    )
    fig.add_annotation(
        text="<b>M</b> = Meaningful &nbsp;&nbsp;|&nbsp;&nbsp; <b>N</b> = Nominal &nbsp;&nbsp;|&nbsp;&nbsp; <b>R</b> = Recruitment",
        xref="paper", yref="paper",
        x=0.5, y=-0.16,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=11, color="#020A0A"),
        align="center",
    )
    fig.add_annotation(
        text="<b>U</b> = Unknown &nbsp;&nbsp;|&nbsp;&nbsp; <b>T</b> = Tangential &nbsp;&nbsp;|&nbsp;&nbsp; <b>M</b> = Meaningful",
        xref="paper", yref="paper",
        x=0.5, y=-0.24,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=11, color="#020A0A"),
        align="center",
    )
    fig.add_annotation(
        text="Engagement",
        xref="paper", yref="paper",
        x=0.5, y=-0.34,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        align="center",
    )
    fig.layout.yaxis2.title.text = ""
    fig.layout.yaxis3.title.text = ""
    return fig


def learning_engagement_output_bubble(df):
    df = df[df["Activity Type"] == "Learning"].copy()
    df["Engagement"] = df["Engagement"].replace({
        "Presentation": "M", "Meaningful": "M", "Nominal": "N", "Recruitment": "R"
    })
    df["Output"] = df["Output"].replace({
        "Unknown": "U", "Tangential": "T", "Meaningful": "M"
    })
    plot_df = (
        df.dropna(subset=["Engagement", "Output", "Scale"])
        .groupby(["Engagement", "Output", "Scale"])
        .size()
        .reset_index(name="Activities")
    )
    scale_order = ["Small", "Medium", "Large"]
    output_order = ["M", "T", "U"]
    fig = px.scatter(
        plot_df, x="Engagement", y="Output", size="Activities",
        color="Scale", facet_col="Scale",
        category_orders={"Scale": scale_order, "Output": output_order},
        size_max=45,
        title="Learning: Engagement vs Output by Scale",
    )
    fig.update_traces(marker=dict(line=dict(width=1, color="black")), opacity=0.8)
    fig.update_xaxes(tickangle=0, title_text="", showline=True, linecolor="#AABBCC", mirror=True, linewidth=1.5)
    fig.update_yaxes(title_text="Output", ticklabelstandoff=15, showline=True, linecolor="#AABBCC", mirror=True, linewidth=1.5)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(
        showlegend=False,
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        plot_bgcolor="#EEF2F7",
        paper_bgcolor="#ffffff",
        margin=dict(l=80, r=40, t=60, b=82),
    )
    fig.add_annotation(
        text="<b>M</b> = Meaningful &nbsp;&nbsp;|&nbsp;&nbsp; <b>N</b> = Nominal &nbsp;&nbsp;|&nbsp;&nbsp; <b>R</b> = Recruitment",
        xref="paper", yref="paper",
        x=0.5, y=-0.16,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=11, color="#020A0A"),
        align="center",
    )
    fig.add_annotation(
        text="<b>U</b> = Unknown &nbsp;&nbsp;|&nbsp;&nbsp; <b>T</b> = Tangential &nbsp;&nbsp;|&nbsp;&nbsp; <b>M</b> = Meaningful",
        xref="paper", yref="paper",
        x=0.5, y=-0.24,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=11, color="#020A0A"),
        align="center",
    )
    fig.add_annotation(
        text="Engagement",
        xref="paper", yref="paper",
        x=0.5, y=-0.34,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        align="center",
    )
    fig.layout.yaxis2.title.text = ""
    fig.layout.yaxis3.title.text = ""
    return fig


def workshops_engagement_output_bubble(df):
    df = df[df["Activity Type"] == "Workshop"].copy()
    df["Engagement"] = df["Engagement"].replace({
        "Presentation": "M", "Meaningful": "M", "Nominal": "N", "Recruitment": "R"
    })
    df["Output"] = df["Output"].replace({
        "Unknown": "U", "Tangential": "T", "Meaningful": "M"
    })
    plot_df = (
        df.dropna(subset=["Engagement", "Output", "Scale"])
        .groupby(["Engagement", "Output", "Scale"])
        .size()
        .reset_index(name="Activities")
    )
    scale_order = ["Small", "Medium", "Large"]
    output_order = ["M", "T", "U"]
    fig = px.scatter(
        plot_df, x="Engagement", y="Output", size="Activities",
        color="Scale", facet_col="Scale",
        category_orders={"Scale": scale_order, "Output": output_order},
        size_max=45,
        title="Workshops: Engagement vs Output by Scale",
    )
    fig.update_traces(marker=dict(line=dict(width=1, color="black")), opacity=0.8)
    fig.update_xaxes(tickangle=0, title_text="", showline=True, linecolor="#AABBCC", mirror=True, linewidth=1.5)
    fig.update_yaxes(title_text="Output", ticklabelstandoff=15, showline=True, linecolor="#AABBCC", mirror=True, linewidth=1.5)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(
        showlegend=False,
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        plot_bgcolor="#EEF2F7",
        paper_bgcolor="#ffffff",
        margin=dict(l=80, r=40, t=60, b=82),
    )
    fig.add_annotation(
        text="<b>M</b> = Meaningful &nbsp;&nbsp;|&nbsp;&nbsp; <b>N</b> = Nominal &nbsp;&nbsp;|&nbsp;&nbsp; <b>R</b> = Recruitment",
        xref="paper", yref="paper",
        x=0.5, y=-0.16,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=11, color="#020A0A"),
        align="center",
    )
    fig.add_annotation(
        text="<b>U</b> = Unknown &nbsp;&nbsp;|&nbsp;&nbsp; <b>T</b> = Tangential &nbsp;&nbsp;|&nbsp;&nbsp; <b>M</b> = Meaningful",
        xref="paper", yref="paper",
        x=0.5, y=-0.24,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=11, color="#020A0A"),
        align="center",
    )
    fig.add_annotation(
        text="Engagement",
        xref="paper", yref="paper",
        x=0.5, y=-0.34,
        showarrow=False,
        font=dict(family="Arial, sans-serif", size=12, color="#020A0A"),
        align="center",
    )
    fig.layout.yaxis2.title.text = ""
    fig.layout.yaxis3.title.text = ""
    return fig

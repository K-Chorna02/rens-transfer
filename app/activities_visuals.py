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
    plot_df["MonthLabel"] = plot_df["Month"].dt.strftime("%b %Y")

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
    month_labels = normalized_df.columns.strftime("%b %Y")
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
    plot_df = (
        df.dropna(subset=["Engagement", "Output", "Scale"])
        .groupby(["Engagement", "Output", "Scale"])
        .size()
        .reset_index(name="Activities")
    )

    scale_order = ["Small", "Medium", "Large"]

    fig = px.scatter(
        plot_df,
        x="Engagement",
        y="Output",
        size="Activities",
        color="Scale",
        facet_col="Scale",
        category_orders={"Scale": scale_order},
        size_max=45,
        title="Activities by Engagement and Output, Faceted by Scale",
    )

    fig.update_traces(
        marker=dict(line=dict(width=1, color="black")),
        opacity=0.8,
    )

    fig.update_xaxes(
        tickangle=45,
        title_text="Engagement",
    )

    fig.update_yaxes(
        title_text="Output",
    )

    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    fig.update_layout(
        showlegend=False,
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

'''
def activity_count(df:pd.DataFrame)->go.Figure:

    # Parse dates (mixed formats allowed)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Extract month name
    df['Month'] = df['Date'].dt.month_name()

    # Count number of activities per month
    monthly_counts = df['Month'].value_counts().reset_index()
    monthly_counts.columns = ['Month', 'ActivityCount']

    # Correct month order
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    monthly_counts['Month'] = pd.Categorical(monthly_counts['Month'], categories=month_order, ordered=True)
    monthly_counts = monthly_counts.sort_values('Month')

    # Line chart
    fig = px.line(
        monthly_counts,
        x="Month",
        y="ActivityCount",
        markers=True,
        title="Monthly Activity Trend (2025)",
        
        template="plotly_white",
        color_discrete_sequence=["#1f77b4"]
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Activities",
        hovermode="x unified"
    )

    return fig


def workstream_activities(df:pd.DataFrame)->go.Figure:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Group activity counts
    ws_scale_counts = df.groupby(['Workstreams', 'Scale']).size().reset_index(name='Count')

    # Stacked bar with correct blue palette
    fig = px.bar(
        ws_scale_counts,
        x='Workstreams',
        y='Count',
        color='Scale',
        title='Activities by Workstream and Scale (2025)',
        barmode='stack',
        template='plotly_white',
        
        color_discrete_sequence=px.colors.sequential.Blues_r  # ✅ FIXED
    )

    fig.update_layout(
        xaxis_title="Workstream",
        yaxis_title="Number of Activities"
    )
    return fig


def type_output_bar(df:pd.DataFrame)->go.Figure:
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # ---------------------------------------
    # 2. Group counts by Activity Type and Output
    # ---------------------------------------
    act_out_counts = (
        df.groupby(['Activity Type', 'Output'])
        .size()
        .reset_index(name='Count')
    )

    # ---------------------------------------
    # 3. Horizontal Stacked Bar Chart
    # ---------------------------------------
    fig = px.bar(
        act_out_counts,
        x='Count',
        y='Activity Type',
        color='Output',
        orientation='h',                   # <-- horizontal
        title='Activity Type vs Output (2025)',
        barmode='stack',
        template='plotly_white',
        color_discrete_sequence=px.colors.sequential.Blues_r  # darker blues
    )

    fig.update_layout(
        xaxis_title="Number of Activities",
        yaxis_title="Activity Type",
        legend_title="Output"
    )
    return fig


def engagement_levels(df =pd.DataFrame)->go.Figure:
    # Parse dates
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Group by workstream and engagement
    ws_eng_counts = (
        df.groupby(['Workstreams', 'Engagement'])
        .size()
        .reset_index(name='Count')
    )

    # Grouped bar chart
    fig = px.bar(
        ws_eng_counts,
        x='Workstreams',
        y='Count',
        color='Engagement',
        barmode='group',                           # <-- grouped, not stacked
        title='Workstream vs Engagement Levels (2025)',
        template='plotly_white',
        color_discrete_sequence=px.colors.sequential.Blues_r  # clean dark blues
    )

    fig.update_layout(
        xaxis_title="Workstream",
        yaxis_title="Number of Activities",
        legend_title="Engagement Level"
    )

    return fig


def access_pie(df = pd.DataFrame)->go.Figure:

    # Count Access values
    access_counts = df['Access'].value_counts().reset_index()
    access_counts.columns = ['Access', 'Count']

    # Pie chart
    fig_access = px.pie(
        access_counts,
        names='Access',
        values='Count',
        title='Access Proportion Across All Activities',
        color_discrete_sequence=px.colors.sequential.Blues_r,   # dark blues
        hole=0.0                                                 # full pie
    )

    fig_access.update_layout(
        template='plotly_white',
    )

    return fig_access


def activity_heatmap(df = pd.DataFrame)->go.Figure:
    ws_counts = df['Workstreams'].value_counts().reset_index()
    ws_counts.columns = ['Workstream', 'Count']
    
    # Number of workstreams
    n = len(ws_counts)
    
    # Determine grid size (square or rectangle close to square)
    grid_size = int(np.ceil(np.sqrt(n)))
    
    # Pad data to fill the grid
    padded_counts = ws_counts['Count'].tolist() + [0] * (grid_size**2 - n)
    padded_labels = ws_counts['Workstream'].tolist() + [""] * (grid_size**2 - n)
    
    # Convert to a matrix
    count_matrix = np.array(padded_counts).reshape(grid_size, grid_size)
    label_matrix = np.array(padded_labels).reshape(grid_size, grid_size)
    
    # Square heatmap
    fig = px.imshow(
        count_matrix,
        color_continuous_scale=px.colors.sequential.Blues_r,
        aspect='equal',  # ensures squares
        text_auto=False  # no numbers on tiles
    )
    
    # Hover tooltips with the correct Workstream name
    fig.update_traces(
        hovertemplate="Workstream: %{customdata}<br>Count: %{z}<extra></extra>",
        customdata=label_matrix
    )
    fig.update_layout(
        title="Workstream Activity Heatmap (Square Tiles)",
        template="plotly_white",
        xaxis_visible=False,
        yaxis_visible=False
    )
    
    return fig
    
    
    
def activity_trend_ex_meetings(df:pd.DataFrame)->go.Figure:
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

   
    df['Activity Type'] = df['Activity Type'].astype(str).str.strip().str.lower()
    df_filtered = df[df['Activity Type'] != 'meeting'].copy()
    
    # ---------------------------------------
    # 4. Extract Month
    # ---------------------------------------
    df_filtered['Month'] = df_filtered['Date'].dt.month_name()
    
    # Keep Jan to Oct only
    month_order = [
        "January", "February", "March", "April", "May",
        "June", "July", "August", "September", "October"
    ]
    df_filtered = df_filtered[df_filtered['Month'].isin(month_order)]
    
    # ---------------------------------------
    # 5. Count activities per month
    # ---------------------------------------
    monthly_counts = (
        df_filtered.groupby("Month")
                   .size()
                   .reindex(month_order)      # ensures correct order
                   .reset_index(name="Count")
    )
    
    fig = px.line(
        monthly_counts,
        x='Month',
        y='Count',
        markers=True,
        title='Activity Trend (Jan–Oct) — Excluding Meetings',
        template='plotly_white',
        color_discrete_sequence=["#1f77b4"],  # Blue line
    )
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Activities",
        hovermode="x unified"
    )
    
    return fig
    
    
    
def meetings_monthly(df):
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    df['Activity Type'] = df['Activity Type'].astype(str).str.strip().str.lower()
    
    df_meetings = df[df['Activity Type'] == 'meeting'].copy()
    
    # ---------------------------------------
    # 4. Extract Month
    # ---------------------------------------
    df_meetings['Month'] = df_meetings['Date'].dt.month_name()
    
    # Filter only Sept–Oct
    target_months = ["September", "October"]
    df_meetings = df_meetings[df_meetings['Month'].isin(target_months)]
    
    # ---------------------------------------
    # 5. Count meetings per month
    # ---------------------------------------
    monthly_counts = (
        df_meetings.groupby('Month')
                   .size()
                   .reindex(target_months)
                   .reset_index(name='Count')
    )
    
    fig = px.line(
        monthly_counts,
        x='Month',
        y='Count',
        markers=True,
        title='Meetings Trend (September–October)',
        template='plotly_white',
        color_discrete_sequence=["#004c99"],  # deep blue
    )
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Meetings",
        hovermode="x unified"
    )
    return fig
    
    
def activity_monthly_trend(df):
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    df['Month'] = df['Date'].dt.month_name()
    
    # Keep only September + October
    target_months = ["September", "October"]
    df_sep_oct = df[df['Month'].isin(target_months)].copy()
    
    # ---------------------------------------
    # 4. Count activities per month
    # ---------------------------------------
    monthly_counts = (
        df_sep_oct.groupby("Month")
                  .size()
                  .reindex(target_months)     # ensure correct order
                  .reset_index(name="Count")
    )
    
    fig = px.line(
        monthly_counts,
        x='Month',
        y='Count',
        markers=True,
        title='Activity Trend (September–October)',
        template='plotly_white',
        color_discrete_sequence=["#1f77b4"],  # blue line
    )
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Activities",
        hovermode="x unified"
    )
    return fig



'''
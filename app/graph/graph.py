from langgraph.graph import END, START, StateGraph

from app.graph.nodes import AnswerNode, RejectNode, SearchNode, ClassifierNode

from app.graph.router import route_after_classification
from app.graph.state import ChatState
from app.search.wikipedia import WikipediaSearchEngine


def build_graph():
    builder = StateGraph(ChatState)

    classifier_node = ClassifierNode()
    reject_node = RejectNode()
    search_node = SearchNode(search_engine=WikipediaSearchEngine())
    answer_node = AnswerNode()

    builder.add_node("classify", classifier_node)
    builder.add_node("reject", reject_node)
    builder.add_node("search", search_node)
    builder.add_node("answer", answer_node)

    builder.add_edge(START, "classify")
    builder.add_conditional_edges(
        "classify", route_after_classification, {"reject": "reject", "search": "search"}
    )

    builder.add_edge("search", "answer")
    builder.add_edge("answer", END)

    return builder.compile()

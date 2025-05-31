# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.toolbox_toolset import ToolboxToolset
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters

_allowed_path = os.path.dirname(os.path.abspath(__file__))
print(f"Allowed path: {_allowed_path}")

root_agent = Agent(
    # model="gemini-2.0-flash",
    model=LiteLlm(model="custom_openai/deepseek-v3"),
    # model=LiteLlm(model="deepseek/deepseek-chat"),
    name="root_agent",
    instruction=f"You are a helpful assistant, designed to assist with customer service tasks. you can operate files in allowed directory {_allowed_path}.",
    # Add Toolbox tools to ADK agent
    tools=[
        ToolboxToolset(
            server_url="http://127.0.0.1:5000", toolset_name="customer-toolset"
        ),
        ToolboxToolset(
            server_url="http://127.0.0.1:5000", toolset_name="service-toolset"
        ),
        MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=[
                    '-y',  # Arguments for the command
                    '@modelcontextprotocol/server-filesystem',
                    _allowed_path,
                ],
            ),
            tool_filter=[
                'read_file',
            #    'read_multiple_files',
                'list_directory',
            #    'directory_tree',
                'search_files',
                'get_file_info',
                'list_allowed_directories',
            ],
        )
    ],
)

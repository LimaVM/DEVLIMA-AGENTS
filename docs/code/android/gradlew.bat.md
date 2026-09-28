# android/gradlew.bat

Wrapper Windows fornecido por Gradle: valida Java, monta argumentos e invoca GradleWrapperMain, preservando exit code.

[Arquivo fonte](../../../android/gradlew.bat) · 94 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>@rem</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L2"></a>2 | <code>@rem Copyright 2015 the original author or authors.</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L3"></a>3 | <code>@rem</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L4"></a>4 | <code>@rem Licensed under the Apache License, Version 2.0 (the &quot;License&quot;);</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L5"></a>5 | <code>@rem you may not use this file except in compliance with the License.</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L6"></a>6 | <code>@rem You may obtain a copy of the License at</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L7"></a>7 | <code>@rem</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L8"></a>8 | <code>@rem      https://www.apache.org/licenses/LICENSE-2.0</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L9"></a>9 | <code>@rem</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L10"></a>10 | <code>@rem Unless required by applicable law or agreed to in writing, software</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L11"></a>11 | <code>@rem distributed under the License is distributed on an &quot;AS IS&quot; BASIS,</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L12"></a>12 | <code>@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L13"></a>13 | <code>@rem See the License for the specific language governing permissions and</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L14"></a>14 | <code>@rem limitations under the License.</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L15"></a>15 | <code>@rem</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L16"></a>16 | <code>@rem SPDX-License-Identifier: Apache-2.0</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L17"></a>17 | <code>@rem</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L18"></a>18 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L19"></a>19 | <code>@if &quot;%DEBUG%&quot;==&quot;&quot; @echo off</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L20"></a>20 | <code>@rem ##########################################################################</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L21"></a>21 | <code>@rem</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L22"></a>22 | <code>@rem  Gradle startup script for Windows</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L23"></a>23 | <code>@rem</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L24"></a>24 | <code>@rem ##########################################################################</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L25"></a>25 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L26"></a>26 | <code>@rem Set local scope for the variables with windows NT shell</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L27"></a>27 | <code>if &quot;%OS%&quot;==&quot;Windows_NT&quot; setlocal</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L28"></a>28 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L29"></a>29 | <code>set DIRNAME=%~dp0</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L30"></a>30 | <code>if &quot;%DIRNAME%&quot;==&quot;&quot; set DIRNAME=.</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L31"></a>31 | <code>@rem This is normally unused</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L32"></a>32 | <code>set APP_BASE_NAME=%~n0</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L33"></a>33 | <code>set APP_HOME=%DIRNAME%</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L34"></a>34 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L35"></a>35 | <code>@rem Resolve any &quot;.&quot; and &quot;..&quot; in APP_HOME to make it shorter.</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L36"></a>36 | <code>for %%i in (&quot;%APP_HOME%&quot;) do set APP_HOME=%%~fi</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L37"></a>37 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L38"></a>38 | <code>@rem Add default JVM options here. You can also use JAVA_OPTS and GRADLE_OPTS to pass JVM options to this script.</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L39"></a>39 | <code>set DEFAULT_JVM_OPTS=&quot;-Xmx64m&quot; &quot;-Xms64m&quot;</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L40"></a>40 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L41"></a>41 | <code>@rem Find java.exe</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L42"></a>42 | <code>if defined JAVA_HOME goto findJavaFromJavaHome</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L43"></a>43 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L44"></a>44 | <code>set JAVA_EXE=java.exe</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L45"></a>45 | <code>%JAVA_EXE% -version &gt;NUL 2&gt;&amp;1</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L46"></a>46 | <code>if %ERRORLEVEL% equ 0 goto execute</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L47"></a>47 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L48"></a>48 | <code>echo. 1&gt;&amp;2</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L49"></a>49 | <code>echo ERROR: JAVA_HOME is not set and no &#x27;java&#x27; command could be found in your PATH. 1&gt;&amp;2</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L50"></a>50 | <code>echo. 1&gt;&amp;2</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L51"></a>51 | <code>echo Please set the JAVA_HOME variable in your environment to match the 1&gt;&amp;2</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L52"></a>52 | <code>echo location of your Java installation. 1&gt;&amp;2</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L53"></a>53 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L54"></a>54 | <code>goto fail</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L55"></a>55 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L56"></a>56 | <code>:findJavaFromJavaHome</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L57"></a>57 | <code>set JAVA_HOME=%JAVA_HOME:&quot;=%</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L58"></a>58 | <code>set JAVA_EXE=%JAVA_HOME%/bin/java.exe</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L59"></a>59 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L60"></a>60 | <code>if exist &quot;%JAVA_EXE%&quot; goto execute</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L61"></a>61 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L62"></a>62 | <code>echo. 1&gt;&amp;2</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L63"></a>63 | <code>echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME% 1&gt;&amp;2</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L64"></a>64 | <code>echo. 1&gt;&amp;2</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L65"></a>65 | <code>echo Please set the JAVA_HOME variable in your environment to match the 1&gt;&amp;2</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L66"></a>66 | <code>echo location of your Java installation. 1&gt;&amp;2</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L67"></a>67 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L68"></a>68 | <code>goto fail</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L69"></a>69 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L70"></a>70 | <code>:execute</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L71"></a>71 | <code>@rem Setup the command line</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L72"></a>72 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L73"></a>73 | <code>set CLASSPATH=%APP_HOME%\gradle\wrapper\gradle-wrapper.jar</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L74"></a>74 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L75"></a>75 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L76"></a>76 | <code>@rem Execute Gradle</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L77"></a>77 | <code>&quot;%JAVA_EXE%&quot; %DEFAULT_JVM_OPTS% %JAVA_OPTS% %GRADLE_OPTS% &quot;-Dorg.gradle.appname=%APP_BASE_NAME%&quot; -classpath &quot;%CLASSPATH%&quot; org.gradle.wrapper.GradleWrapperMain %*</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L78"></a>78 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L79"></a>79 | <code>:end</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L80"></a>80 | <code>@rem End local scope for the variables with windows NT shell</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L81"></a>81 | <code>if %ERRORLEVEL% equ 0 goto mainEnd</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L82"></a>82 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L83"></a>83 | <code>:fail</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L84"></a>84 | <code>rem Set variable GRADLE_EXIT_CONSOLE if you need the _script_ return code instead of</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L85"></a>85 | <code>rem the _cmd.exe /c_ return code!</code> | Comentário/orientação do arquivo; não acrescenta uma configuração ativa. |
| <a id="L86"></a>86 | <code>set EXIT_CODE=%ERRORLEVEL%</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L87"></a>87 | <code>if %EXIT_CODE% equ 0 set EXIT_CODE=1</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L88"></a>88 | <code>if not &quot;&quot;==&quot;%GRADLE_EXIT_CONSOLE%&quot; exit %EXIT_CODE%</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L89"></a>89 | <code>exit /b %EXIT_CODE%</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L90"></a>90 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L91"></a>91 | <code>:mainEnd</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L92"></a>92 | <code>if &quot;%OS%&quot;==&quot;Windows_NT&quot; endlocal</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |
| <a id="L93"></a>93 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L94"></a>94 | <code>:omega</code> | Comando/estrutura do wrapper de ferramenta; o contexto acima identifica seu executor. |

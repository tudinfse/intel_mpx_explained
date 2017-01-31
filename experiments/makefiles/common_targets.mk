# headers
%.h: %.H
	$(M4) $(M4FLAGS) $(MACROS) $^ > $(BUILD_PATH)/$@

# object files
$(BUILD_PATH)/%.$(OBJ_EXT): %.c
	$(CC) $(CCOMFLAGS) $(CFLAGS) -c $< -o $@ $(INCLUDE)

$(BUILD_PATH)/%.$(OBJ_EXT): %.C
	$(CC) $(CCOMFLAGS) $(CFLAGS) -c $< -o $@ $(INCLUDE)

$(BUILD_PATH)/%.$(OBJ_EXT): %.cpp
	$(CXX) $(CCOMFLAGS) $(CXXFLAGS) -c $< -o $@ $(INCLUDE)

$(BUILD_PATH)/%.$(OBJ_EXT): %.cxx
	$(CXX) $(CCOMFLAGS) $(CXXFLAGS) -c $< -o $@ $(INCLUDE)

$(BUILD_PATH)/%.$(OBJ_EXT): %.cc
	$(CXX) $(CCOMFLAGS) $(CXXFLAGS) -c $< -o $@ $(INCLUDE)

# executable
$(BUILD_PATH)/$(NAME): $(LLS)
	$(CXX) $(CCOMFLAGS) $(CXXFLAGS) -o $@ $^ $(INCLUDE) $(INCLUDE_LIB_DIRS) $(LIBS)

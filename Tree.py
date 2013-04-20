class CommentTree(object):

	def __init__(self, selfName, selfLinkId, selfParentName, isRroot = False):
		self.children = []
		self.parent_node = None;
		self.id = None;
		self.name = selfName;
		self.link_id = selfLinkId;
		self.parent_name = selfParentName;
		self.author_name = None;
		self.author_id = None; 
		self.subreddit = None;
		self.upvotes = None; 
		self.downvotes = None; 
		self.score  = None; 
		self.created = None; 
		self.edited = None; 
		self.num_reports  = None;
		self.isRoot = isRroot;
	
	def set_attributes(self, comment):
		self.id = comment[0];
		# self.name = selfName;
		# self.link_id = selfLinkId;
		# self.parent_name = selfParentName;
		self.author_name = comment[4]; 
		self.author_id   = comment[5]; 
		self.subreddit   = comment[8];
		self.upvotes     = comment[9]; 
		self.downvotes   = comment[10]; 
		self.score       = comment[11]; 
		self.created     = comment[12]; 
		self.edited      = comment[13]; 
		self.num_reports = comment[14];

	def get_degree_sequence(self):
		# assumes that we have a big tree for each post
		rootsChildren = list(self.children);
		degrees = [];
		for child in rootsChildren:
			degrees.append(len(child.children) + 1 );
			for ch in child.children:
				rootsChildren.append(ch)
		return degrees


	def get_height_sequence(self):
		# assumes that we have a big tree for each post
		rootsChildren = list(self.children);
		hgh = 1;
		heights = [];
		while True:
			temp=[];
			for child in rootsChildren:
				heights.append(hgh);
				for ch in child.children:
					temp.append(ch)
			
			if temp == []:
				break;
			rootsChildren = list(temp);
			hgh = hgh+ 1 ;
		return heights
	
	
	def get_height_of_node(self, node):
		rootsChildren = list(self.children);
		hgh = 1;
		while True:
			temp=[];
			for child in rootsChildren:
				if child.name == node.name:
					return hgh;
				for ch in child.children:
					temp.append(ch);
			if temp == []:
				break;
			rootsChildren = list(temp);
			hgh += 1 ;
		return 0
	
	def get_shortest_path(self, node1, node2):
		h1 = self.get_height_of_node(node1);
		h2 = self.get_height_of_node(node2);
		path = 0;
		if h1 < h2:
			dif = h2 - h1;
			while dif > 0:
				node2 = node2.parent_node;
				dif = dif - 1;
				path = path + 1;
		elif h1 > h2:
			dif = h1 - h2;
			while dif > 0:
				node1 = node1.parent_node;
				dif = dif - 1;
				path = path + 1;
		
		while not node1 == node2:
			node1 = node1.parent_node
			node2 = node2.parent_node
			path += 2 ;
		return path
		
	
	def get_average_path_length(self):
		rootsChildren = list(self.children);
		for child in rootsChildren:
			for ch in child.children:
				rootsChildren.append(ch);
		PL = 0;
		count = 0;
		for i in range(0,len(rootsChildren)):
			for j in range(i+1, len(rootsChildren)):
				if rootsChildren[i] == rootsChildren[j]:
					continue;
				PL += self.get_shortest_path(rootsChildren[i],rootsChildren[j]);
				count += 1;
		if count == 0 :
			return [0, 0, 0]
		APL = (1.0*PL) / count;
		return [APL, PL , count];
		
		
	def get_number_of_nodes(self):
		rootsChildren = list(self.children);
		nodes = 0;
		for child in rootsChildren:
			nodes = nodes + 1 ;
			for ch in child.children:
				rootsChildren.append(ch)
		return nodes

	def get_number_of_edges(self):
		return self.get_number_of_nodes() - 1;

	def get_max_width(self):
		rootsChildren = list(self.children);
		max_width = 0;
		max_height = 0;
		hgh = 1;
		while True:
			tmp_width = 0;
			temp = [];
			for child in rootsChildren:
				tmp_width = tmp_width + 1;
				for ch in child.children:
					temp.append(ch);
			rootsChildren = list(temp);
			if max_width < tmp_width:
				max_width = tmp_width;
				max_height = hgh;				
			hgh = hgh + 1;
			if temp == []:
				break;		
		return [max_height, max_width] # returns the height which has the maximum width
		
	def get_number_of_leaves(self):
		seq = self.get_degree_sequence();
		print seq
		num = 0;
		for s in seq:
			if s == 1:
				num = num + 1;
		return num;
		
		
	def get_leaves_of_height(self, height):
		rootsChildren = list(self.children);
		if height < 1:
			return 0;
		hgh = 1;
		heights = [];
		while True:
			if height == hgh:
				break;
			temp=[];
			for child in rootsChildren:
				for ch in child.children:
					temp.append(ch);
			if temp == []:
				return 0;
			rootsChildren = list(temp);
			hgh = hgh + 1 ;	
		leave = 0;
		for s in rootsChildren:
			if len(s.children) == 0 :
				leave = leave + 1;
		return leave;
	
	def get_number_of_unique_users(self):
		rootsChildren = list(self.children);
		users = [];
		for child in rootsChildren:
			if child.author_name not in users:
				users.append(child.author_name);			
			for ch in child.children:
				rootsChildren.append(ch);
		return len(users);
		
	
		
		
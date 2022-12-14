public class String {
	String trim();
	String toUpperCase();
	String replaceAll(String regex, String replacement);
	int codePointBefore(int index);
	static String valueOf(boolean b);
	boolean regionMatches(int toffset, String other, int ooffset, int len);
	String toString();
	int compareToIgnoreCase(String str);
	static String valueOf(boolean b);
	void getChars(int srcBegin, int srcEnd, char[] dst, int dstBegin);
	char charAt(int index);
	boolean contentEquals(CharSequence cs);
	static String valueOf(char c);
	int compareToIgnoreCase(String str);
	boolean endsWith(String suffix);
	static String copyValueOf(char[] data, int offset, int count);
	static String valueOf(char[] data);
	String toUpperCase();
	int indexOf(String str, int fromIndex);
	boolean matches(String regex);
	static String copyValueOf(char[] data, int offset, int count);
	String toUpperCase();
	boolean isEmpty();
	static String format(Locale l, String format, Object... args);
	static String valueOf(char[] data, int offset, int count);
	String toUpperCase(Locale locale);
	String replaceAll(String regex, String replacement);
	byte[] getBytes(Charset charset);
	static String valueOf(double d);
	String replace(char oldChar, char newChar);
	String toString();
	void getChars(int srcBegin, int srcEnd, char[] dst, int dstBegin);
	static String valueOf(double d);
	int hashCode();
	char charAt(int index);
	int indexOf(int ch, int fromIndex);
	static String valueOf(float f);
	int codePointBefore(int index);
	int lastIndexOf(String str);
	static String format(String format, Object... args);
	String[] split(String regex, int limit);
	int codePointBefore(int index);
	String[] split(String regex, int limit);
	void getBytes(int srcBegin, int srcEnd, byte[] dst, int dstBegin);
	boolean startsWith(String prefix);
	String toLowerCase();
	String trim();
	int hashCode();
	boolean startsWith(String prefix, int toffset);
	boolean matches(String regex);
	String replaceAll(String regex, String replacement);
	byte[] getBytes();
}
